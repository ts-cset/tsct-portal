from flask import g, session
import pytest
from portal.db import get_db


def test_edit(client):
    assert client.get('/courseManagement').status_code == 302

    response = client.post(
        '/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/courseManagement')
        response2 = client.get('/courseManagement')
        assert response.headers['Location'] == 'http://localhost/courseManagement'
        assert client.get('/courseManagement').status_code == 200
        assert session['user_id'] == 1
        assert g.user['email'] == 'teacher@stevenscollege.edu'
        assert b'<h2>Course Management<h2>' in response2.data
        assert b'+' in response2.data


def test_create_course(client):
    assert client.get('/courseCreate').status_code == 200
    response = client.get('/courseCreate')
    assert b'+' in response.data
