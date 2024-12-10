import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error


param_names = ['period','competency','weight','comp_performance']

def get_ARIMA(train : pd.DataFrame, test : pd.DataFrame, order = (2,3,2), alpha = 0.05, target='comp_performance') -> pd.DataFrame:
    '''
    Función para el calculo de las proyecciones de series de tiempo ARIMA

    Parámetros:

    train - Es el DataFrame que contiene la parte seleccionada para ser la data de entrenamiento del modelo.

    test - Es el DataFrame que contiene la parte seleccionada para ser la data de pruebas del modelo.

    target - Es el nombre de la columna analizada para la generación de las predicciones.

    El método retorna:

    Un DataFrame con las proyecciones de series de tiempo ARIMA.
    '''
    try:
      # acá separamos nuestra data a analizar
      y = train[target]#self.target

      # y la utilizamos para ingresarla en el modelo
      ARIMAmodel = ARIMA(y, order = order)

      ARIMAmodel = ARIMAmodel.fit(method_kwargs={'disp':0,'warn_convergence':False},)

      # Acá generamos otro set de datos que contenga las predicciones realizadas con
      # el modelo ARIMA
      y_pred_b = ARIMAmodel.get_forecast(len(test.index))
      y_pred_df_b = y_pred_b.conf_int(alpha = alpha)
      y_pred_df_b["Predictions"] = ARIMAmodel.predict(start = y_pred_df_b.index[0], end = y_pred_df_b.index[-1])
      y_pred_df_b["period"] = test['period'].values
      y_pred_df_b['index'] = test.index
      # y_pred_out_b = y_pred_df_b["Predictions"]

      ARIMA_out = y_pred_df_b

      return ARIMA_out
    except Exception as error:
      raise ValueError(f'could not get ARIMA prediction for {target}:', error)

def get_ARMA(train : pd.DataFrame, test : pd.DataFrame, order = (1,0,1), alpha = 0.05, target='comp_performance') -> pd.DataFrame:
  '''
  Función para el calculo de las proyecciones de series de tiempo ARMA

  Parámetros:

  train - Es el DataFrame que contiene la parte seleccionada para ser la data de entrenamiento del modelo.

  test - Es el DataFrame que contiene la parte seleccionada para ser la data de pruebas del modelo.

  target - Es el nombre de la columna analizada para la generación de las predicciones.

  El método retorna:

  Un DataFrame con las proyecciones de series de tiempo ARMA.
  '''
  try:
    # print('Setting y')
    # acá separamos nuestra data a analizar
    y = train[target]#self.target]
    # print('y: ')
    # print(y.head())

    # print('Fitting mod')
    # y la utilizamos para ingresarla en el modelo
    mod = SARIMAX(y, order = order)
    fit = mod.fit(disp=0)

    # print('Forecasting')
    # print('len(test.index)')
    # print(len(test.index))
    # print(test)
    # Acá generamos otro set de datos que contenga las predicciones realizadas con
    # el modelo ARMA
    y_pred = fit.get_forecast(len(test.index)) # type: ignore
    # print('y_pred:')
    # print(type(y_pred))
    # print(y_pred)

    # print('Confidence interval dataframe')
    y_pred_df = y_pred.conf_int(alpha = alpha)
    # print('y_pred_df')
    # print(y_pred_df)

    # print('Predictions')
    y_pred_df["Predictions"] = fit.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1]) # type: ignore
    # print(y_pred_df['Predictions'])
    # print('period values')
    # print(test['period'].values)
    y_pred_df["period"] = test['period'].values
    # print(y_pred_df['period'])
    y_pred_df.index = test.index # type: ignore 
    # print(y_pred_df.index) # type: ignore

    # print('y_pred_dg predictions')
    # print(y_pred_df.head())

    # y_pred_out = y_pred_df["Predictions"]

    # print(y_pred_df)
    # print('ARMA_out')
    ARMA_out = y_pred_df
    # print('ARMA_out')
    # print(y_pred_df.head()) # type: ignore

    return ARMA_out # type: ignore
  except Exception as error:
    raise ValueError(f'could not get ARMA prediction for {target}:', error)


def get_SARIMAX(train : pd.DataFrame, test : pd.DataFrame, order = (5,4,2), alpha = 0.05, seasonal_order=(3,1,1,12),target='comp_performance') -> pd.DataFrame:
  '''
  Función para el calculo de las proyecciones de series de tiempo SARIMAX

  Parámetros:

  train - Es el DataFrame que contiene la parte seleccionada para ser la data de entrenamiento del modelo.

  test - Es el DataFrame que contiene la parte seleccionada para ser la data de pruebas del modelo.

  target - Es el nombre de la columna analizada para la generación de las predicciones.

  El método retorna:

  Un DataFrame con las proyecciones de series de tiempo SARIMAX.
  '''
  try:
    # acá separamos nuestra data a analizar
    y = train[target]#self.target]


    mod = SARIMAX(y, order = order, seasonal_order=seasonal_order, trend='ct')
    mod = mod.fit(disp=0)

    # Acá generamos otro set de datos que contenga las predicciones realizadas con
    # el modelo SARIMAX
    y_pred_c : PredictionResults = mod.get_forecast(len(test.index)) # type: ignore
    y_pred_df_c = pd.DataFrame(y_pred_c.conf_int(alpha = alpha))

    y_pred_df_c["Predictions"] = mod.predict(start = y_pred_df_c.index[0], end = y_pred_df_c.index[-1]) # type: ignore
    y_pred_df_c["period"] = test['period'].values
    y_pred_df_c.index = test.index
    # y_pred_out_c = y_pred_df_c["Predictions"]

    # print(y_pred_df_c)
    SARIMAX_out = y_pred_df_c

    return pd.DataFrame(SARIMAX_out)
  except Exception as error:
    raise ValueError(f'could not get SARIMAX prediction for {target}:', error)


def get_rmse(test : pd.DataFrame | None, predictions : pd.DataFrame | None, target : str = 'comp_performance' , pred_target : str = "Predictions") -> float:
  if predictions is None or test is None:
    raise ValueError('could not get the rmse for the current test data')
  try:
    return round(float(np.sqrt(mean_squared_error(test[target], predictions[pred_target]))),2)
  except Exception as error:
    raise ValueError('could not get the rmse for the current test data, ', error)
  return 1.0
