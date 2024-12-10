from data.db import DB_API
from src.forecasting.course_predictor import CoursePerformancePredictor
from src.forecasting.comp_predictor import CompPerformancePredictor
from models.student import Student

from fastapi import FastAPI
import dotenv
import os

_db = DB_API(test = True)

def test_get_students() -> list[Student]:
    students = _db.get_students()
    assert len(students) >= 1
    return students

students = test_get_students()

def get_predictions(student: Student):
    current_period = student.periods[-1].period.replace('-','')

    # print(student.periods[-1].period.replace('-',''))

    student_data = student.to_frame().reset_index(drop=True)
    print("student_data")
    print(student_data)

    cpp = CompPerformancePredictor(student_data)
    # print("cpp")
    # print(cpp.forecast_competency_performance())

    cspp = CoursePerformancePredictor(student_data, cpp.forecast_competency_performance())

    predictions = cspp.forecast_courses_performance(current_period)
    print("predictions")
    print(predictions)

    _db.update_student_data(student.student_id, student.institution_id, predictions)


for student in students:
    get_predictions(student)


# dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


# try:
#     env_batch_size = os.getenv('BATCH_SIZE')
#     batch_size : int = int(str(env_batch_size))
# except:
#     batch_size = 100

# db = DB_API()

# api = FastAPI()

# @api.get("/")
# def read_root():
#     return {"Hello": "World"}

# @api.get("/ai/health")
# def health():
#     return {"status": "ok"}

# @api.get("/ai/student_forecasts/{institution_id}")
# def read_student_forecasts(institution_id: str):
#     current_period = db.get_latest_period(institution_id)

#     current_batch = 0
#     total_current_students = db.get_student_count(institution_id)
#     batch_data = []

#     for _ in range(total_current_students // batch_size):
#         students = db.get_students(institution_id, current_batch)

#         for student in students:
#             student_data = db.get_student_data(student.student_id, institution_id).to_frame()
#             _cpp = cpp(student_data)
#             _cspp = cspp(student_data, _cpp.forecast_competency_performance())

#             predictions = _cspp.forecast_courses_performance(current_period)

#             db.update_student_data(student.student_id, institution_id, predictions)

#             batch_data.append(predictions)

#         current_batch += 1
        




#     pass

# @api.get("/student_forecast/{institution_id}/{student_id}")
# def read_student_forecast(institution_id: str, student_id: str):
#     '''
#     This funtion is going to be called by the main api to get the forecasted data for the student.
#     '''
#     pass


# # first step: when the time comes, the main api is going to make a request to this service top generate the predictions opf the student data for the current period.
# # This will always happen in the background during the maintenance of both the academic application of the institution and SIPEFCA's service.
# # for this we will 

