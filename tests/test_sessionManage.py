from flask import g, session
import pytest
from portal.db import get_db
import os
import tempfile
from test_courseEditor import login, logout


def test_edit_roster(client):
    """Tests the editSession page with a specific session
    of the course 180 to see if functionallity works"""
    assert client.get('/courseSessions/180/edit/0').status_code == 302

    rv = login(
        client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data

    with client:
        client.get('/courseSessions/180/edit/0').status_code == 200

        response = client.get('/courseSessions/180/edit/0')
        assert b'Edit Software Project 2-A' in response.data

        response2 = client.post('/courseSessions/180/edit/0', data={ 'editStudents': ['bobphillup191@stevenscollege.edu']


        }, follow_redirects=True)
        assert b'Course Sessions' in response2.data

        rv = logout(client)
        assert b'TSCT Portal Login' in rv.data



def test_createSession(client):
    """Tests access of the createSession page and the
    form dat to see if you can successfully create a session
    in a specific course"""

    assert client.get('/createSession/course/180').status_code == 302

    rv = login(
        client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data

    with client:
        client.get('/createSession/course/180') == 200

        response = client.get('/createSession/course/180')
        assert b'Create a New Session in Software Project 2'

        response2 = client.post('/createSession/course/180', data={'students': [5, 6, 7]},
        follow_redirects=True)
        assert b'Software Project 2-C' in response2.data

        rv = logout(client)
        assert b'TSCT Portal Login' in rv.data


def test_sessionManage(client):
    """Tests the data on the session Manage page of zach fedors
    Software Project 2 sessions"""

    assert client.get('/course/180/sessions').status_code == 302

    rv = login(
        client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data

    with client:
        response = client.get('/course/180/sessions')
        assert b'<h2>Session Management for Software Project 2' in response.data
        assert b'Click the + below to create a new session' in response.data
        assert b'Software Project 2-A' in response.data

        rv = logout(client)
        assert b'TSCT Portal Login' in rv.data
