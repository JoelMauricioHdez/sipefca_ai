from data import *
import os
import json
from models.student import Student
from models.period import Period

_db = db.DB_API(test = True)

def test_get_students():
    students = _db.get_students()
    print(students)
    assert len(students) == 1