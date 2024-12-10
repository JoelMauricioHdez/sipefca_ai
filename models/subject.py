from pandas import DataFrame
from models.competence import Competence

class Subject:
    def __init__(self, id: str = '', credits: int = 0, competencies: list[Competence] = [], grade: int = 0, predicted_grades: int = 0, json : dict | None = None):
        assert id != '' or json is not None
        if json is not None:
            self.from_json(json)
            return 
        self.id = id
        self.credits = credits
        self.grade = grade
        self.predicted_grade = grade
        self.competencies = []

    def get_numerical_grade(self, grade: str):
        if grade is None:
            return 0
        grade_map = {'A': 4.0, 'B+':3.5,'B': 3.0,'C+': 2.5, 'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': 0.0, 'R': -1.0}
        try:
            numerical_grade = grade_map[grade]
            return numerical_grade
        except Exception as error:
            raise ValueError(f'could not get the numerical grade for the subject: {error}')

    def from_json(self, subject_data: dict):
        try:
            pred_grade = subject_data['predicted_grade']
        except:
            pred_grade = 0
        try:
            self.id = subject_data['course_id']
            self.credits = subject_data['credits']
            self.grade = self.get_numerical_grade(subject_data['grade'])
            self.predicted_grade = pred_grade
            self.competencies = []
            for competency in subject_data['competences']:
                self.competencies.append(Competence(json=competency))
        except Exception as error:
            raise ValueError(f'could not load the subject data from the json: {error}')
    def get_competencies(self):
        return self.competencies

    def __str__(self):
        return f"Subject: {self.id} with credits: {self.credits} and competencies: {self.competencies}"

    def __repr__(self):
        return f'Subject(id="{self.id}", credits="{self.credits}", competencies="{self.competencies}", grade="{self.grade}")'
