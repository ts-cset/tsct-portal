import pytest
from flask import g, session
from portal.db import get_db

# When doing a GET request we should get a status code of 200 back
def test_teacher_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.teacher_login()
    # Until a template is created the response when logging in with teacher is Hello teacher
    assert b'Hello teacher' in response.data

    #with client:
        #client.get('/teacher-page')
        #assert session['user_id'] == 1
        #assert g.user['email'] == 'teacher@stevenscollege.edu'

def test_student_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.student_login()
    assert b'hello student' in response.data

    #with client:
        #client.get('/teacher-page')
        #assert session['user_id'] == 1
        #assert g.user['email'] == 'teacher@stevenscollege.edu'

# This attempts to 'login' with an incorrect email or password. Does it for both email or password so both error messages are tested
@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('teacher@stevenscollege.edu', 'test', b'Incorrect username or password.'),
    ('test', 'qwerty', b'Incorrect username or password.'),
))
def test_teacher_login_validate_input(auth, email, password, message):
    response = auth.teacher_login(email, password)
    assert message in response.data

def test_logout(client, auth):
    auth.teacher_login()

    with client:
        auth.logout()
        assert 'user_id' not in session
