import pytest
from flask import g, session
from portal.db import get_db

def test_home(client, auth):
    # Attempt to visit page without logging in
    response = client.get('/teacher/home')
    # Non-authorized users should be redirected to login
    assert 'http://localhost/' == response.headers['Location']
    # Log in as a teacher
    auth.teacher_login()
    response = client.get('/teacher/home')
    # Logged-in teachers should not be redirected
    assert b'Manage Courses' in response.data

def test_courses(client, auth):
    auth.teacher_login()
    response = client.get('/teacher/courses')
    # Check that mock course exists
    assert b'Big Software Energy' in response.data
    # Attempt to delete mock course
    response = client.post(
        '/teacher/courses',
        data={1:1}
    )
    # Check that mock course no longer exists
    assert b'Big Software Energy' not in response.data

def test_creation(client, auth):
    auth.teacher_login()
    #Makes sure that you can go to Class Creation
    assert client.get('/teacher/courses/create').status_code == 200
    #Fills out the form in Class Creation
    response = client.post(
        '/teacher/courses/create',
        data={'code': 180, 'name': 'Software Project II', 'major': 'CSET',
        'description': 'A basic computer course'}
    )
    #Asserts that it's switched over to the Course Selection
    assert 'http://localhost/teacher/courses' == response.headers['Location']

def test_make_session(client, auth):
    auth.teacher_login()
    response = client.get('teacher/session/create')
    assert 'http://localhost/teacher/home' == response.headers['Location']
    response = client.post(
        '/teacher/session/create',
        data={'session':1}
    )
    assert b'Lueklee, Kevstice' in response.data

def test_session_add(client, auth):
    auth.teacher_login()

    # Get requests should be redirected away
    response = client.get('/teacher/session/add')
    assert 'http://localhost/teacher/session/create' == response.headers['Location']

    # Session creation must be underway to add students to the roster for it
    # otherwise the user will simply be redirected away
    response = client.post(
        '/teacher/session/add',
        data={1:1}
    )
    assert 'http://localhost/teacher/session/create' == response.headers['Location']

    # Now we begin creating a session
    client.post(
        '/teacher/session/create',
        data={'session':1}
    )
    # Students may then be added with checkbox interface
    response = client.post(
        '/teacher/session/add',
        data={1:1}
    )
    # Confirm that session_add redirects to session page after running
    assert 'http://localhost/teacher/session/create' == response.headers['Location']
    response = client.get('/teacher/session/create')
    # Confirm that the roster is not empty
    assert b'Remove from Session' in response.data

def test_session_submit(client, auth):
    auth.teacher_login()

    # If a user tries to use the GET method at the submit URL, they should be
    # redirected to the session creation interface
    response = client.get('/teacher/session/submit')
    assert 'http://localhost/teacher/session/create' == response.headers['Location']

    # Session creation must be underway to add students to the roster for it
    # otherwise the user will simply be redirected away
    response = client.post(
        '/teacher/session/submit',
        data={'session_name': 'A', 'meeting_days': 'MTWThF'}
    )
    assert 'http://localhost/teacher/session/create' == response.headers['Location']

    client.post(
        '/teacher/session/create',
        data={'session':1}
    )

    # If the user successfully submits the post request, they should be redirected
    # to the appropriate page
    response = client.post(
        '/teacher/session/submit',
        data={'session_name': 'A', 'meeting_days': 'MTWThF'}
    )
    assert 'http://localhost/teacher/home' == response.headers['Location']

def test_session_cancel(client, auth):
    auth.teacher_login()

    # If the user tries to cancel a session when one does not exist, they will be
    # redirected away
    response = client.get('/teacher/session/cancel')
    assert 'http://localhost/teacher/home' == response.headers['Location']

    
    # The user begins creation of a session
    client.post(
        '/teacher/session/create',
        data={'session':1}
    )
    # The user cancels creation of a session
    response = client.get('/teacher/session/cancel')
    assert 'http://localhost/teacher/home' == response.headers['Location']
    # If the user now tries to view the session creation window, they will be
    # redirected to the teacher home
    response = client.get('/teacher/session/create')
    assert 'http://localhost/teacher/home' == response.headers['Location']
