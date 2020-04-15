from flask import g, session
import pytest
from portal.db import get_db
import os
import tempfile
from test_course_editor import login, logout


def test_edit_session(client):
    """Tests the editSession page with a specific session
    of the course 180 to see if functionallity works"""
    assert client.get('/courseSessions/180/edit/21').status_code == 302

    rv = login(
        client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data

    with client:
        client.get('/courseSessions/180/edit/21').status_code == 200

        response = client.get('/courseSessions/180/edit/21')
        assert b'Edit Session CSET-180-A' in response.data

        response_2 = client.post('/courseSessions/180/edit/21', data={ 'editName': 'Software Project 2-A',
        'editTimes': '12:30 is the time', 'editRoom': '105', 'editLocal': 'Greenfield'
        }, follow_redirects=True)
        assert b'Sessions for course Software Project 2' in response_2.data
        assert b'Software Project 2-A' in response_2.data

        rv = logout(client)
        assert b'TSCT Portal Login' in rv.data



def test_create_session(client):
    """Tests access of the createSession page and the
    form dat to see if you can successfully create a session
    in a specific course"""

    assert client.get('/createSession/course/180/').status_code == 302

    rv = login(
        client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data

    with client:
        client.get('/createSession/course/180/') == 200

        response = client.get('/createSession/course/180/')
        assert b'Create a New Session in Software Project 2'

        response_2 = client.post("/createSession/course/180/", data={ 'sessionTitle': 'Software Project 2-C',
        'sessionTimes': '12:30 is the time', 'roomNumber': '105', 'locations': 'Greenfield' },
        follow_redirects=True)
        assert b'Sessions for course Software Project 2' in response_2.data
        assert b'Software Project 2-C' in response_2.data
        assert b'Click the + below to create a new session' in response_2.data

        rv = logout(client)
        assert b'TSCT Portal Login' in rv.data


def test_course_sessions(client):
    """Tests the data on the session Manage page of zach fedors
    Software Project 2 sessions"""

    assert client.get('/courseSessions/180').status_code == 302

    rv = login(
        client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data

    with client:
        response = client.get('/courseSessions/180')
        assert b'<h2>Sessions for course Software Project 2' in response.data
        assert b'<h4>Click the + below to create a new session</h4>' in response.data
        assert b'CSET-180-A' in response.data

        rv = logout(client)
        assert b'TSCT Portal Login' in rv.data

#Starter Tests for roster

# def test_create_roster(client):
#     """Tests the creation of the student roster"""
#     assert client.get('/courseSession/180/rosterCreate/4').status_code == 302
#
#     rv = login(
#         client, 'teacher@stevenscollege.edu', 'qwerty')
#     assert b'Logged in' in rv.data
#
#     with client:
#         response = client.get('courseSession/180/rosterCreate/4')
#         assert b'<h2>Roster for session CSET-180-B<h2>' in response.data
#         assert b'Students' in response.data
#         assert b'Save' in response.data
#
#
#
#
# def test_edit_roster(client):
#     """Tests the edit of a sessions student roster"""
#     assert client.get('/courseSession/180/rosterEdit/2').status_code == 302
#
#     rv = login(
#         client, 'teacher@stevenscollege.edu', 'qwerty')
#
#     assert b'Logged in' in rv.data
#
#     with client:
#         response = client.get('courseSession/180/rosterEdit/2')
#         assert b'<h2>Roster for session CSET-180-A' in response.data
#         assert b'Students' in response.data
#         assert b'Save' in response.data
