from flask import g, session
import pytest
from portal.db import get_db


def test_edit(client):
    # Getting the courseEdit should return redirect
    assert client.get('/courseEdit/180').status_code == 302

    response = client.post(
        '/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

    with client:
        response = client.get('/courseEdit/180')
        assert response.headers['Location'] == 'http://localhost/courseEdit/180'
        assert client.get('/courseEdit/180').status_code == 200
        assert b'Course title' in response.data
        assert b'save' in response.data


def test_create_course(client):
    assert client.get('/createCourse').status_code == 302

    response = client.post(
        '/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

    with client:
        response = client.get('/courseCreate')
        assert response.headers['Location'] == 'http://localhost/courseEdit/1'
        assert client.get('/courseManagement').status_code == 200
        assert b'Course title' in response.data
        assert b'save' in response.data
