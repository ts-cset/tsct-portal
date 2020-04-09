import pytest
from flask import g, session
from portal.db import get_db

def test_student_home(client, auth):
    response =  client.get('/student/home')
    assert 'http://localhost/' == response.headers['Location']
    auth.student_login()
    response = client.get('/student/home')
    assert b'<li>CSET</li>' in response.data
