import json
import os
from dotenv import dotenv_values
from pandas import DataFrame
import requests

from models.student import Student


class DB_API:
    def __init__(self, test : bool = False):
        self.test = test
        if not self.test:
            self.__load_env__()
            res = self.__login__()

    def __load_env__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            print('loading .env file')
            config = dotenv_values(dotenv_path)
            self.host = config.get('HOST')
            self.port = config.get('DB_PORT')
            self.username =  config.get('DB_USER')
            self.key = config.get('DB_KEY')
            self.url = f'http://{self.host}:{self.port}/'

    def __login__(self):
        try:
            response = requests.post(f'{self.url}login', json={'username': self.username, 'key': self.key}, headers={'Content-Type': 'application/json'})
        except Exception as error:
            raise ValueError(f'could not login to the database: {error}')

        if response.status_code != 200:
            raise ValueError(f'could not login to the database, status code: {response.status_code}')

        return response.json()
    
    def get_student_data(self, student_id: str, institution_id: str = "INTEC"):
        data = Student("test", "INTEC")

        return data

    def get_students(self, institution_id: str = "INTEC", pagination : int = 0) -> list[Student]: 
        students : list[Student] = []

        dir = os.path.dirname(__file__).replace('data','docs')
        if self.test:
            with open(f'{dir}/test_data.json', 'r') as f:
                data = f.read()
                students.append(Student(json=json.loads(data)))
        
        return students

    def get_student_count(self, institution_id: str = "INTEC"): 
        return 2000
    
    def update_student_data(self, student_id: str, institution_id: str, data: DataFrame):
        pass

    def get_latest_period(self, institution_id: str = "INTEC"):
        return '2024-04'
    

    


