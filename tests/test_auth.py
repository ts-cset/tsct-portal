import pytest
from flask import g, session
from portal.db import get_db
from portal.auth import validate, validate_text, validate_date, validate_number

def test_teacher_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.teacher_login()
    assert 'http://localhost/teacher/home' == response.headers['Location']

def test_student_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.student_login()
    assert 'http://localhost/student/home' == response.headers['Location']
    response = client.get('/teacher/home')
    assert 'http://localhost/' == response.headers['Location']

# This attempts to 'login' with an incorrect email or password. Does it for both email or password so both error messages are tested
@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('teacher@stevenscollege.edu', 'test', b'Incorrect username or password.'),
    ('test', 'qwerty', b'Incorrect username or password.'),
))
def test_teacher_login_validate_input(auth, email, password, message):
    response = auth.teacher_login(email, password)
    assert message in response.data

def test_logout(client, auth, app):
    auth.teacher_login()
    with client:
        auth.logout()
        assert 'user_id' not in session

def test_validate():
    # Validate called with an unexpected table name should return False without
    # attempting to connect to database
    assert not validate(5, 'nonetable')

def test_validate_text():
    # String input should be considered based on given max length length
    assert validate_text('Some text', 20) == True
    assert validate_text('Some text', 4) == False

def test_validate_number():
    # Number input should be considered by value even if passed as a string
    assert validate_number('12', 15, min=3) == True
    assert validate_number('12', 3) == False

    # String input that cannot be coverted to a number should return false
    assert validate_number('Eleven', 15) == False

def test_validate_date():
    # Dates should be in standard HTML parsed date format, yyyy-mm-dd
    assert validate_date('2020-04-28') == True
    assert validate_date('04-28-2020') == False

    # Certain invalid dates are not allowed (note: currently, days outside of a
    # month's standard range are still allowed, eg 2020-02-31)
    assert validate_date('2020-00-00') == False
