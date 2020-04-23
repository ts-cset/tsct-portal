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

def test_grade_assignments(client, auth,app):
    auth.teacher_login()
    response = client.get('/teacher/grade/submission')
    assert response.status_code == 302
    with app.app_context():
        assert client.post('/teacher/grade/submission', data={'grade-submission' : 100, 'submission': "(2, 1)"}).status_code == 302
        with get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT * FROM assignment_grades
                """)
                res = cur.fetchone()
                assert res[2] == '100'
        client.post('/teacher/grade/submission', data={'grade-submission' : 200, 'submission': "(2, 1)"})
        with get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT * FROM assignment_grades
                """)
                res = cur.fetchone()
                assert res[2] == '200'

def test_view_assignments(client,auth):
    auth.teacher_login()

    assert client.post('/teacher/assignments/view', data={'view-grade': 1}).status_code == 200
    assert b'List of assignments' in client.post('/teacher/assignments/view', data={'view-grade': 1}).data
    response = client.get('/teacher/assignments/view')
    assert response.status_code == 302

def test_grade(client,auth,app):
    auth.teacher_login()
    with app.app_context():
        assert client.post('/teacher/assignments/grade', data={'grade': 1}).status_code == 200
        assert b'Kevstice--Lueklee' in client.post('/teacher/assignments/grade', data={'grade': 1}).data
        response = client.get('/teacher/assignments/grade')
        assert response.status_code == 302
