import pandas as pd
from sklearn.linear_model import LinearRegression

class CoursePerformancePredictor():
  '''
  Clase para el calculo de las proyecciones de desempeño académico de los estudiantes.

  Parámetros:

  data - Es el DataFrame inicial con los datos historicos del estudiante.

  predicted_comp_performance - Es el DataFrame con los datos de las proyecciones
  de desempeño de las competencias. Origindario de la clase CompPerformancePredictor.

  Métodos:

  forecast_courses_performance - Método para la generación de las proyecciones de
  desempeño académico en las distintas asignaturas de un periodo en particular.

  predict_course_performance - Método para la generación de las preddicciones de
  desempeño académico de una asignatura.

  '''

  def __init__(self, data: pd.DataFrame, predicted_comp_performance: pd.DataFrame):
    self.data = data
    self.predicted_comp_performance = predicted_comp_performance

  def forecast_courses_performance(self,period:str,df: pd.DataFrame | None = None):
    '''
    Método para la generación de las proyecciones de desempeño académico en las
    distintas asignaturas de un periodo en particular.

    Parámetros:
    period - Periodo del cual se desean generar las proyecciones.

    df - Es un DataFrame opcional para pasar un set de datos con los datos
    de las predicciones de desempeño de las competencias y el desempeño
    logrado por el estudiante en los periodos anteriores. El valor por
    defecto es el DataFrame original que posee el objeto
    CoursePerformancePredictor.

    Este método retorna un DataFrame que contiene los datos actualizados de
    las asignaturas del periodo seleccionado incluyendo el desempeño proyectado
    para cada una.
    '''
    if df is None:
      df = self.data

    try:
      period_df = df[df['period'] == period]

      courses_performance = []

      # print('periods')
      # print(period_df['course_id'].unique())

      for course in period_df['course_id'].unique():
        courses_performance.append(self.predict_course_performance(course,df))

      # print(courses_performance)

      return pd.concat(courses_performance)
    except Exception as e:
      raise Exception(f"Error in predict_courses_performance: {e}")

  def predict_course_performance(self, course: str, df: pd.DataFrame | None = None,):
    '''
    Método para la generación de las preddicciones de desempeño académico de una
    asignatura.

    Parámetros:
    course - Cadena de texto que represente el código de asignatura.

    df - Es un DataFrame opcional para pasar un set de datos con los datos
    de las predicciones de desempeño de las competencias y el desempeño
    logrado por el estudiante en los periodos anteriores. El valor por
    defecto es el DataFrame original que posee el objeto
    CoursePerformancePredictor.

    Este método retorna un DataFrame con los datos de la asignatura en cuestión.
    '''
    if df is None:
      df = self.data

    try:
      print("Course Performance Prediction")

      course_data = df[df['course_id'] == course]
      # print("Course Data")
      # print(course_data)
      period = course_data['period'].unique()[0]
      # print('period')
      # print(period)

      competences = []

      for competence in course_data['competency'].unique():
        weight = (course_data[course_data['competency'] == competence]['weight']
                  .unique()[0])
        # print("Weight")
        # print(weight)
        grade = (course_data[course_data['competency'] == competence]['numerical_grade']
                .unique()[0])
        # print("Grade")
        # print(grade)

        pred_perf = self.predicted_comp_performance[self.predicted_comp_performance['competency'] == competence]
        pred_perf['weight'] = weight
        pred_perf['numerical_grade'] = grade

        # print("Predicted Competency Performance")
        # print(pred_perf)

        competences.append(pred_perf[pred_perf['period'] == period])

      # print("Competency Performance Prediction")
      # print(competences)

      comp_df = pd.concat(competences)
      # print(comp_df)

      wavg_pred = self.__get_weighted_avg(comp_df) * 4
      # print("Weighted avg prediciton: ", self.get_weighted_avg(comp_df) * 4)
      mvlr_pred = self.__get_regressed_course_performance(comp_df, self.data)
      # print("Grade predicition: ", self.__get_regressed_course_performance(comp_df, self.data))

      course_data['predicted_grade'] = (wavg_pred + mvlr_pred) / 2
      course_data['predicted_grade'] = course_data['predicted_grade'].clip(upper=4.0)
      # course_data.clip(lower{'predicted_grade': 4.0}, inplace=True)

      return course_data
    except Exception as e:
      raise Exception(f"Error en predict_course_performance: {e}")

  def __get_weighted_avg(self, df: pd.DataFrame):
    '''
    Método para el cálculo del promedio pesado de las proyecciones de estudiantes.

    Esta permite calcular el desempeño académico directamente en base a las
    predicciones de desempeño en las competencias de la asignatura.

    Parámetros:
    df - Es un DataFrame que contiene los datos referentes a una asignatura
    determinada.

    Valor retornado:
    La función retorna un valor numérico que representa el desempeño académico
    proyectado de la asignatura en cuestión.
    '''
    comp_weight = 0
    weights = 0
    for competency in df['competency'].unique():
      comp_perf = df[df['competency'] == competency]['comp_performance'].unique()[0]
      weight = df[df['competency'] == competency]['weight'].unique()[0]
      comp_weight += comp_perf * weight
      weights += weight

    return round(comp_weight/weights, 2)

  def __get_regressed_course_performance(self, target: pd.DataFrame,df: pd.DataFrame | None = None):
    '''
    Esta función es para conseguir las predicciones de desempeño académico
    en la asignatura basado en las predicciones generadas de las competencias
    manejadas para el periodo.

    Parámetros:
    Target - Es un DataFrame que contiene los datos referentes a una asignatura
    determinada.

    df - Es un DataFrame opcional para pasar un set de datos con los datos
    de las predicciones de desempeño de las competencias y el desempeño
    logrado por el estudiante en los periodos anteriores.

    Valor retornado:
    La función retorna un valor numérico que representa el desempeño académico
    proyectado de la asignatura en cuestión.
    '''
    if df is None:
      df = self.data

    # comp_map = {'C1':1,'C2':2,'C3':3,'C4':4,'C5':5,'C6':6}

    # print('df')
    # print(df.head())

    # print('target')
    # print(target.head())

    # df['competency_'] = df['competency'].apply(lambda x: comp_map[x])

    X = df[['comp_performance','weight']]
    y = df['numerical_grade']

    regr = LinearRegression()
    regr.fit(X,y)

    target_X = []
    for competency in target['competency'].unique():
      t = target[target['competency'] == competency].copy()
      # print(t.head())
      target_weight = t['weight'].unique()[0]
      target_comp_perf = t['comp_performance'].unique()[0]

      target_X.append([target_comp_perf,target_weight])


    df = pd.DataFrame(target_X)

    return round(regr.predict(df)[0],2)
