import pytest
from flask import g, session, url_for, request
from portal.db import get_db
from urllib.parse import urlparse
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

def test_course_edit(client,auth,app):
    auth.teacher_login()
    #assert client.get('/teacher/courses/edit').status_code == 200
    #response = client.post(
        ##data={'course_code': '5527', 'course_name': 'CSET-180', 'major': 'CSET', 'description': 'Not empty.'}
    ##assert 'http://localhost/teacher/courses' == response.headers['Location']
    response = client.get('teacher/courses/1/edit')
    assert b'Course-Edit' in response.data
    with app.app_context():
        res = client.post(
            '/teacher/courses/1/edit',
            data={'code': 500, 'name': 'Ice-Cream', 'major': 'CSET',
            'description': 'A basic introduction to Ice-Cream'}
        )
        with get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT * FROM courses
                WHERE id = %s
                """,
                (1, )
                )
                result = cur.fetchone()
                assert result['course_name'] == 'Ice-Cream'
                assert res.headers['Location'] == 'http://localhost/teacher/courses'
def test_sessions(client, auth):
    auth.teacher_login()
    assert client.get('/teacher/session').status_code == 200


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

    # Session creation must be underway to add students to the roster for that session
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

def test_session_remove(client, auth):
    auth.teacher_login()

    # Get requests should be redirected away
    response = client.get('/teacher/session/remove')
    assert 'http://localhost/teacher/session/create' == response.headers['Location']

    # Session creation must be underway to remove students from the roster
    # otherwise the user will simply be redirected away
    response = client.post(
        '/teacher/session/remove',
        data={1:1}
    )
    assert 'http://localhost/teacher/session/create' == response.headers['Location']

    # Now we begin creating a session
    client.post(
        '/teacher/session/create',
        data={'session':1}
    )
    # Students need to be added before they can be removed
    client.post(
        '/teacher/session/add',
        data={1:1}
    )
    # The added student can be removed
    client.post(
        'teacher/session/remove',
        data={1:1}
    )

    response = client.get('/teacher/session/create')
    # In the test case, the roster for this session should now be empty
    assert b'Remove from Session' not in response.data

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
    assert 'http://localhost/teacher/session' == response.headers['Location']

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

def test_session_edit(client, auth, app):
    auth.teacher_login()

    # If the user tries to visit the edit page without an edit in progress,
    # They should be redirected to the teacher home view
    response = client.get('/teacher/session/edit')
    assert 'http://localhost/teacher/home' == response.headers['Location']

    # The user should be able to begin a new editing session by posting a session code
    response = client.post(
        '/teacher/session/edit',
        data={'edit':1}
    )
    # They should then see the editing page
    assert b'Edit a Session' in response.data

def test_edit_mode(client, auth):
    auth.teacher_login()

    # A user begins editing a post
    client.post(
        '/teacher/session/edit',
        data={'edit':1}
    )

    # Adding and removing from the roster, canceling, and submitting
    # should behave differently when an edit is in progress

    response = client.get('/teacher/session/add')
    assert 'http://localhost/teacher/session/edit' == response.headers['Location']

    response = client.get('/teacher/session/remove')
    assert 'http://localhost/teacher/session/edit' == response.headers['Location']

    response = client.get('/teacher/session/submit')
    assert 'http://localhost/teacher/session/edit' == response.headers['Location']

    client.get('/teacher/session/cancel')
    response = client.get('/teacher/home')
    assert b'Session edit canceled' in response.data
