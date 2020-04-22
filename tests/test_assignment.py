import pytest
from flask import g, session
from portal.db import get_db

def test_assignments(client, auth):
    auth.teacher_login()

    # Test data assignment should appear in assignment list
    response = client.get('/teacher/assignments')
    assert b'Bigger Software' in response.data

    # Test assignment should be deleted if checked box is submitted
    response = client.post(
        '/teacher/assignments',
        data={'id': 2}
    )
    assert b'Bigger Software' not in response.data

def test_edit_assignments(client, auth):
    auth.teacher_login()

    # On GET request, user should be redirected
    response = client.get('/teacher/assignments/edit')
    assert 'http://localhost/teacher/assignments' == response.headers['Location']

    # On POST request, user should see an edit page with forms pre-filled with
    # current data from database
    response = client.post(
        '/teacher/assignments/edit',
        data={'edit': 2}
    )
    assert b'value="Bigger' in response.data

def test_submit_assignments(client, auth):
    auth.teacher_login()

    # On GET request, user should be redirected
    response = client.get('/teacher/assignments/submit')
    assert 'http://localhost/teacher/assignments' == response.headers['Location']

    # Client should be able to post updates to change database entry
    client.post(
        '/teacher/assignments/submit',
        data={'name': 'Biggerest', 'description': 'And besterest', 'points': 500, 'submit': 2}
    )
    # Data for the second assignment should now be updated
    response = client.get('/teacher/assignments')
    assert b'Biggerest' in response.data

def test_create_assignments(client, auth, app):
    auth.teacher_login()

    # On a GET request, user should see a form for creating new assignments
    response = client.get('/teacher/assignments/create')
    assert b'Assignment Creation' in response.data

    # On POST, user should be able to insert new assignments into the database
    client.post(
        '/teacher/assignments/create',
        data={'name': 'Wumbo Software', 'description': 'I wumbo, you wumbo, he, she, it... wumbo.',
              'points': 900, 'course': 1}
    )
    with app.app_context():
        with get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM assignments WHERE id = 5")
                assert cur.fetchone()['name'] == 'Wumbo Software'

def test_assign_work(client, auth):
    auth.teacher_login()

    # GET requests are redirected
    response = client.get('/teacher/assignments/assign')
    assert 'http://localhost/teacher/sessions' == response.headers['Location']

    # On POST, user should be able to see assignments that belong to posted course id
    # but only ones that have not been assigned already
    response = client.post(
        '/teacher/assignments/assign',
        data={'session_id': 1}
    )
    assert b'Mondo Software' in response.data
    assert b'Bigger Software' not in response.data

def test_assign_submit(client, auth, app):
    auth.teacher_login()

    # GET requests are redirected
    response = client.get('/teacher/assignments/assign/submit')
    assert 'http://localhost/teacher/sessions' == response.headers['Location']

    # On POST, user should be able to insert assignments into the session_assignments
    # junction table with a due date
    response = client.post(
        '/teacher/assignments/assign/submit',
        data={'date': '2020-05-08', 'session_id': 1, 'assign_id': 4}
    )
    with app.app_context():
        with get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM session_assignments where assignment_id = 4 AND session_id = 1
                """)
                assert cur.fetchone() is not None
