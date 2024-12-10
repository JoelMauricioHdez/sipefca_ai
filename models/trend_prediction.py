from pandas import DataFrame

class TrendPrediction:
    def __init__(self, pred : DataFrame = DataFrame(), rmse : float = 1): 
        self.pred = pred
        self.rmse = rmse

    def __str__(self):
        return f"Trend Prediction: {self.pred} with rmse: {self.rmse}"