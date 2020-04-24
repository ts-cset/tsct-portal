import pytest
from flask import g, session
from portal.db import get_db
from portal.auth import validate

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

def test_validate(auth, app, client):
    # Validate called with an unexpected table name should return False without
    # attempting to connect to database
    assert not validate(5, 'nonetable')
