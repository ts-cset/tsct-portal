import pytest
from flask import g, session
from portal.db import get_db


def test_creation(client, auth, app):
    #Logs in as teacher using mock database
    auth.teacher_login('teacher@stevenscollege.edu', 'qwerty')
    #Makes sure that you can go to Class Creation
    assert client.get('/teacher/courses').status_code == 200
    #Fills out the form in Class Creation
    response = client.post('/teacher/courses/create', data={'number': 180, 'name': 'Software Project II', 'major': 'CSET',  'description': 'A basic computer course'})
    #Asserts that it's switched over to the Course Selection
    assert 'http://localhost/courses/' == response.headers['Location']
