import pandas as pd
import numpy as np
from ..time_series import * 
from models.trend_prediction import TrendPrediction 

class CompPerformancePredictor():
  '''
  Clase para la generación de las predicciones de desempeño del estudiante
  en las competencias.

  Parámetros:

  data - Es el DataFrame inicial con los datos historicos del estudiante.

  pred_data - Version formateada del set de datos para la generación de
  las proyecciones.
  '''
  def __init__(self, data: pd.DataFrame):
    self.data : pd.DataFrame = data
    self.pred_data : pd.DataFrame = self.get_weighted_avg(self.data)


  def forecast_competency_performance(self, df: pd.DataFrame | None = None):
    """
    Método para realizar las proyecciones de desempeño de las competencias
    basado en el Time Series Forecasting.

    Parámetros:
    df - Es un DataFrame opcional para pasar un set de datos con los datos
    de las predicciones de desempeño de las competencias.

    El método retorna:

    Un DataFrame con las proyecciones de desempeño de las competencias.

    Estructura del DataFrame:
    {
      index: int,
      period: str,
      competency: str,
      comp_performance: float
    }
    """
    if df is None:
      if self.pred_data is None:
        df = self.data
        df = self.get_weighted_avg(df)
      else:
        df = self.pred_data
    else:
      df = self.data
      df = self.get_weighted_avg(df)

    results = []

    for competency in df['competency'].unique():
      # print('current_comp: ',competency)
      competency_regs = df[df['competency'] == competency].reset_index(drop=True)
      # print(f'comp {competency} regs: ')
      # print(competency_regs.head())

      # get predicted performance for the target period
      results.append(self.get_predicted_comp_performance(competency_regs))

    merged_df = pd.concat(results)

    merged_df = merged_df.sort_values(by=['period','competency']).reset_index(drop=True)

    # Return forecasted data as a DataFrame
    return merged_df

  def get_weighted_avg(self, df: pd.DataFrame | None = None):
    '''
    Retorna el set de datos agrupado por periodos y competencias,
    incluyendo el promedio "pesado" de cada competencia de las
    asignaturas existentes en un determinado perido.

    función necesaria para preparar los datos para la generación de las
    predicciones del desempeño académico del estudiante
    '''
    if df is None:
      df = self.data

    try:
      df = df[df['credits'] > 0]

      # print(df.groupby(['period','competency']))
      df = (df
            .groupby(['period','competency'])
            .apply(lambda x: (x['comp_performance'] * (x['credits'] * x['weight'])).sum() / (x['credits'] * x['weight']).sum())
            .reset_index())

      df.rename(columns={0: 'comp_performance'}, inplace=True)

      return df
    except Exception as error:
      raise (error)

  def get_predicted_comp_performance(self, df: pd.DataFrame, target: str = 'comp_performance', diff:int=2):
    '''
    Retorna el desempeño predecido del estudiante en de un determinado set de datos.

    El parametro "df" debe ser un DataFrame de pandas que contenga unicamente los
    valores de sobre la competencia de la cual se desean hacer las predicciones.
    '''
    if df is None:
      raise ValueError('df cannot be None')

    # print('Received df: ')
    # print(df)

    # define test and train data
    train = df[df.index <= len(df.period.values) - diff].copy()
    # print('training data set: ')
    # print(train)

    test = df[df.index >= len(df.period.values) - diff].copy()
    # print('testing data set: ')
    # print(test)

    # try to get predicted performance with each method type
    try:
      pred = self.get_prediction_rmse(train,test,target)

      # print('pre test')
      # print(test.head())

      # print('pred')
      # print(pred.head)

      # # we get the predicted data and asign its values to the
      # for period in test['period'].unique():
      test.loc[test.period.isin(pred['period']),'comp_performance'] = pred['Predictions'].values

      # print('test ')
      # print(test.head())
      # print()
      # print()
      # print()

      # test.drop(test.index == len(df.period.values) - diff)
      result = pd.concat([train,test[test.index != len(df.period.values) - diff]])

      return result 

    except ValueError as error:
      print("Error predicting the performance for the target competency,", error)
      return


  def get_prediction_rmse(self,train : pd.DataFrame, test: pd.DataFrame, target: str = 'comp_performance',) -> pd.DataFrame:
    '''
    Método para las predicciones de los distintos modelos de series de tiempo
    y sus respectivos valores de rmse para comprobar el nivel de "certeza" de
    las predicciones.

    Parámetros:

    train - Es el DataFrame que contiene la parte seleccionada para ser la data de entrenamiento del modelo.

    test - Es el DataFrame que contiene la parte seleccionada para ser la data de pruebas del modelo.

    target - Es el nombre de la columna analizada para la generación de las predicciones.

    Este método retorna un un diccionario con las siguientes propiedades:

    - pred - El DataFrame con la información de las proyecciones generadas.
    - rmse - El valor del rmse de las predicciones.

    '''
    pred_a = TrendPrediction()
    pred_b = TrendPrediction()
    pred_c = TrendPrediction()

    try:
      # sf = TrendSeriesForcaster(target)
      # print('ARMA')
      pred_a.pred = get_ARMA(train,test,target=target)
      # print("a: ",pred_a.pred.head())
      pred_a.rmse = get_rmse(test,pred_a.pred)
      # print('ARMA rmse: ',pred_a.rmse)


      if pred_a.rmse > 0.05:
         lowest = pred_a

        #  print('ARIMA')
         pred_b.pred = get_ARIMA(train,test,target=target)
        #  print("b: ",pred_b.pred.head())
         pred_b.rmse = get_rmse(test,pred_b.pred)
        #  print('ARIMA rmse: ',pred_b.rmse)



         if pred_b.rmse > 0.05:
            if pred_b.rmse < lowest.rmse:
              lowest = pred_b
            
            # print('SARIMAX')
            pred_c.pred = get_SARIMAX(train,test,target=target)
            # print("c",pred_c.pred.head())
            pred_c.rmse = get_rmse(test,pred_c.pred)
            # print('SARIMAX rmse: ',pred_c.rmse)



            if pred_c.rmse > 0.05:
              if pred_c.rmse < lowest.rmse:
                lowest = pred_c
            else:
              return pd.DataFrame(pred_c.pred)
         else:
            return pd.DataFrame(pred_b.pred)
      else:
        return pd.DataFrame(pred_a.pred)
      return lowest.pred
    except Exception as error:
      raise ValueError('there was an error trying to get the predictions, ', error)
      return {"error": error}
