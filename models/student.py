import random
from pandas import DataFrame, concat
from .period import Period


class Student:
    def __init__(self, student_id : str = '', institution_id : str = '', periods : list[Period] = [], json: dict | None = None): 
        assert student_id != '' or json is not None
        if json is not None:
            self.from_json(json)
            return
        self.student_id = student_id
        self.institution_id = institution_id
        self.periods : list[Period] = periods

    def from_json(self, student_data: dict) :
        try:
            self.student_id = student_data['student_id']
            self.institution_id = student_data['institution_id']
            periods = []
            for period in student_data['periods']:
                periods.append(Period(json=period))
            self.periods = periods

        except Exception as error:
            raise ValueError(f'could not load the student data from the json: {error}')

    def from_frame(self, student_data : DataFrame):
        student = Student(student_data.student_id[0], student_data.institution_id[0], student_data.current_period[0])
        for period in student_data.periods:
            student.periods.append(Period(period.period[0], period.courses[0], period.cant_courses[0], period.total_credits[0]))
        
        self.student_id = student_data.student_id[0]
        self.institution_id = student_data.institution_id[0]            

        return student

    def to_frame(self):
        frames = []
        for period in self.periods: 
            for course in period.courses:
                for competency in course.competencies:
                    frame = {}
                    frame['period'] = period.period.replace('-','')
                    frame['course_id'] = course.id
                    frame['credits'] = course.credits
                    frame['numerical_grade'] = course.grade
                    frame['predicted_grade'] = course.predicted_grade
                    frame['competency'] = competency.id
                    frame['weight'] = competency.weight
                    frame['performance'] = (course.grade / 4.0) * 100
                    frame['comp_performance'] = competency.predicted_performance
                    frames.append(frame)
        return DataFrame(frames)

        # return DataFrame(self.periods)

    def __str__(self):
        return f"Student: {self.student_id} with periods: {self.periods}"
    
    def __repr__(self):
        return f'Student(student_id="{self.student_id}", institution_id="{self.institution_id}, periods:"{self.periods})"'   