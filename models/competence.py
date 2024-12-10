from pandas import DataFrame


class Competence:
    def __init__(self, id : str = '', weight : int = 100, performance : float = 0.0, predicted_performance : float = 0.0, json : dict | None = None):
        assert id != '' or json is not None
        if json is not None:
            self.from_json(json)
            return
        self.id = id
        self.weight = weight
        self.performance = performance
        self.predicted_performance = predicted_performance

    def from_json(self, competency_data: dict):
        try:
            perf = competency_data['performance']
            pred_perf = competency_data['predicted_performance']
        except:
            perf = 100
            pred_perf = 90
        try:
            self.id = competency_data['comp_id']
            self.weight = competency_data['weight']
            self.performance = perf
            self.predicted_performance = pred_perf
        except Exception as error:
            raise ValueError(f'could not load the competency data from the json: {error}') 

    def __str__(self):
        return f"Competence: {self.id} with weight: {self.weight}"

    def __repr__(self):
        return f'Competence(comp_id="{self.id}", weight="{self.weight}")' 
