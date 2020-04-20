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
