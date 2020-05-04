import pytest
from flask import g, session, url_for, request
from portal.db import get_db

def test_sessions(client, auth):
    auth.teacher_login()

    # Teachers should see session from mock data on session page
    response = client.get('/teacher/sessions')
    assert b'180 A' in response.data

    # Teachers should be able to delete sessions using a POST request
    client.post(
        '/teacher/sessions',
        data={'id': 1}
    )
    response = client.get('/teacher/sessions')
    # Session 1 should now be deleted and no longer shown
    assert b'180 A' not in response.data

    # Teachers should not able able to delete sessions they don't own
    response = client.post(
        '/teacher/sessions',
        data={'id': 3}
    )
    assert b'Something went wrong.' in response.data


def test_make_session(client, auth):
    auth.teacher_login()

    # On a GET request where session creation is not underway, users should be
    # redirected to the courses page
    response = client.get('teacher/sessions/create')
    assert 'http://localhost/teacher/courses' == response.headers['Location']

    # Teachers should be able to begin creating a session via POST request
    response = client.post(
        '/teacher/sessions/create',
        data={'course_id': 1}
    )
    # Teacher should see a student's name if session creation begins successfully
    assert b'Lueklee, Kevstice' in response.data

    # Cancel the session creation before next request
    client.get('teacher/sessions/cancel')

    # Teachers should not be able to create sessions for courses they don't own
    client.post(
        '/teacher/sessions/create',
        data={'course_id': 4}
    )
    response = client.get('/teacher/courses')
    assert b'Something went wrong.' in response.data

def test_session_add(client, auth):
    auth.teacher_login()

    # Get requests should be redirected away
    response = client.get('/teacher/sessions/add')
    assert 'http://localhost/teacher/sessions/create' == response.headers['Location']

    # Session creation must be underway to add students to the roster for that session
    # otherwise the user will simply be redirected away
    response = client.post(
        '/teacher/sessions/add',
        data={'id':2}
    )
    assert 'http://localhost/teacher/sessions/create' == response.headers['Location']

    # Now we begin creating a session
    client.post(
        '/teacher/sessions/create',
        data={'course_id':1}
    )

    # Teachers should not be able to add teachers to the roster
    client.post(
        '/teacher/sessions/add',
        data={'id': 3}
    )
    response = client.get('teacher/sessions/create')
    assert b'Something went wrong.' in response.data

    # Students may then be added with checkbox interface
    response = client.post(
        '/teacher/sessions/add',
        data={'id':2}
    )
    # Confirm that session_add redirects to session page after running
    assert 'http://localhost/teacher/sessions/create' == response.headers['Location']
    response = client.get('/teacher/sessions/create')
    # Confirm that the roster is not empty
    assert b'Remove from Session' in response.data

def test_session_remove(client, auth):
    auth.teacher_login()

    # Get requests should be redirected away
    response = client.get('/teacher/sessions/remove')
    assert 'http://localhost/teacher/sessions/create' == response.headers['Location']

    # Session creation must be underway to remove students from the roster
    # otherwise the user will simply be redirected away
    response = client.post(
        '/teacher/sessions/remove',
        data={'id':2}
    )
    assert 'http://localhost/teacher/sessions/create' == response.headers['Location']

    # Now we begin creating a session
    client.post(
        '/teacher/sessions/create',
        data={'course_id':1}
    )

    # Teachers shouldn't be able to attempt to remove invalid users from the table
    client.post(
        'teacher/sessions/remove',
        data={'id':3}
    )
    response = client.get('/teacher/sessions/create')
    assert b'Something went wrong.' in response.data

    # Students need to be added before they can be removed
    client.post(
        '/teacher/sessions/add',
        data={'id':2}
    )
    # The added student can be removed
    client.post(
        'teacher/sessions/remove',
        data={'id':2}
    )

    response = client.get('/teacher/sessions/create')
    # In the test case, the roster for this session should now be empty
    assert b'Remove from Session' not in response.data

def test_session_submit(client, auth):
    auth.teacher_login()

    # If a user tries to use the GET method at the submit URL, they should be
    # redirected to the session creation interface
    response = client.get('/teacher/sessions/submit')
    assert 'http://localhost/teacher/sessions/create' == response.headers['Location']

    # Session creation must be underway to submit other information to finalize it,
    # otherwise the user will simply be redirected away
    response = client.post(
        '/teacher/sessions/submit',
        data={
            'session_name': 'A',
            'meeting_days': 'MTWThF',
            'meeting_place': 'Mellor',
            'meeting_time': '12-4:30'
        }
    )
    assert 'http://localhost/teacher/sessions/create' == response.headers['Location']

    client.post(
        '/teacher/sessions/create',
        data={'course_id':1}
    )

    # If the user successfully submits the post request, they should be redirected
    # to the appropriate page
    response = client.post(
        '/teacher/sessions/submit',
        data={
            'session_name': 'A',
            'meeting_days': 'MTWThF',
            'meeting_place': 'Mellor',
            'meeting_time': '12-4:30'
        }
    )
    assert 'http://localhost/teacher/sessions' == response.headers['Location']

    # If the user attempts to submit invalid data (excessive text length)
    # it should not be sent to the database
    # Re-start session creation
    client.post(
        '/teacher/sessions/create',
        data={'course_id':1}
    )
    # Post some invalid data
    client.post(
        '/teacher/sessions/submit',
        data={
            'session_name': 'A',
            'meeting_days': 'MTWThF',
            'meeting_place': 'This text is way too long for this field',
            'meeting_time': '12-4:30'
        }
    )
    # Get a page that will display the warning that should be flashed
    response = client.get('teacher/courses')
    assert b'Something went wrong.' in response.data

def test_session_cancel(client, auth):
    auth.teacher_login()

    # If the user tries to cancel a session when one does not exist, they will be
    # redirected away
    response = client.get('/teacher/sessions/cancel')
    assert 'http://localhost/teacher/home' == response.headers['Location']


    # The user begins creation of a session
    client.post(
        '/teacher/sessions/create',
        data={'course_id':1}
    )
    # The user cancels creation of a session
    response = client.get('/teacher/sessions/cancel')
    assert 'http://localhost/teacher/home' == response.headers['Location']
    # If the user now tries to view the session creation window, they will be
    # redirected to the courses page
    response = client.get('/teacher/sessions/create')
    assert 'http://localhost/teacher/courses' == response.headers['Location']

def test_session_edit(client, auth, app):
    auth.teacher_login()

    # If the user tries to visit the edit page without an edit in progress,
    # They should be redirected to the teacher home view
    response = client.get('/teacher/sessions/edit')
    assert 'http://localhost/teacher/home' == response.headers['Location']

    # The user should be able to begin a new editing session by posting a session code
    response = client.post(
        '/teacher/sessions/edit',
        data={'edit':1}
    )
    # They should then see the editing page
    assert b'Edit a Session' in response.data

    # Cancel edit to prepare for next request
    client.get('/teacher/sessions/cancel')

    # Teachers should not be able to edit sessions they do not own
    client.post(
        '/teacher/sessions/edit',
        data={'edit': 3}
    )
    response = client.get('teacher/home')
    assert b'Something went wrong.' in response.data

def test_edit_mode(client, auth):
    auth.teacher_login()

    # A user begins editing a post
    client.post(
        '/teacher/sessions/edit',
        data={'edit':1}
    )

    # Adding and removing from the roster, canceling, and submitting
    # should behave differently when an edit is in progress

    response = client.get('/teacher/sessions/add')
    assert 'http://localhost/teacher/sessions/edit' == response.headers['Location']

    response = client.get('/teacher/sessions/remove')
    assert 'http://localhost/teacher/sessions/edit' == response.headers['Location']

    response = client.get('/teacher/sessions/submit')
    assert 'http://localhost/teacher/sessions/edit' == response.headers['Location']

    client.get('/teacher/sessions/cancel')
    response = client.get('/teacher/home')
    assert b'Session edit canceled' in response.data
