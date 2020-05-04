import pytest
from flask import g, session
from portal.db import get_db

def test_student_home(client, auth):
    response = client.get('/student/home')
    assert 'http://localhost/' == response.headers['Location']
    auth.student_login()
    response = client.get('/student/home')
    assert b'Big Software Energy' in response.data

# Test function to check if assignments are assigned to students properly
def test_assignments(client, auth):
    auth.student_login()
    response = client.get('/student/assignments')
    assert 'http://localhost/student/home' == response.headers['Location']
    response = client.post('/student/assignments', data={'session_id': 1})
    assert b'<h2>Big Software</h2>' in response.data

    # Students should not be able to view assignments for sessions they do not
    # belong to
    response = client.post(
        '/student/assignments',
        data={'session_id': '3'}
    )
    assert 'http://localhost/student/home' in response.headers['Location']
    response = client.get('/student/home')
    assert b'Something went wrong.' in response.data

def test_graded_assignments(client, auth):
    auth.student_login()
    response = client.get('/student/grades')
    assert 'http://localhost/student/home' == response.headers['Location']
    response = client.post('/student/grades', data={'session_id': 1})
    assert b'<p>Points: 150/200</p>' in response.data
