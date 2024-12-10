from pandas import DataFrame
from .subject import Subject

class Period:
    def __init__(self, period : str = '', courses : list[Subject] = [], cant_courses : int = 0, total_credits : int = 0, json : dict | None = None):
        assert period != '' or json is not None
        if json is not None:
            self.from_json(json)
            return
        self.period = period
        self.courses = courses
        self.cant_courses = cant_courses
        self.total_credits = total_credits        
    
    def from_json(self, period_data: dict):
        try:
            self.period = period_data['period']
            self.courses = []
            for course in period_data['courses']:
                self.courses.append(Subject(json=course))
            self.cant_courses = period_data['cant_courses']
            self.total_credits = period_data['total_credits']
        except Exception as error:
            raise ValueError(f'could not load the period data from the json: {error}')


    def __str__(self):
        return f"Period: {self.period} with courses: {self.courses}"    
    
    def __repr__(self):
        return f'Period(period="{self.period}", courses="{self.courses}", cant_courses="{self.cant_courses}", total_credits="{self.total_credits}")'