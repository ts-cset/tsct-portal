import pytest


def test_view_sessions(client, auth):
    # getting the form as a logged in users
    auth.login()
    response = client.get('/1/sessions')
    assert b'Sessions' in response.data


def test_create_session(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/sessions/create')
    assert b'Add Session to Course :' in response.data

    response = client.post('/sessions/create', data={
        'courses': 'ENG 101',
        'session_days': 'M/W/F',
        'class_time': '7:00am'})

    assert '/sessions' in response.headers['Location']
    # response = client.get('/sessions')
    # assert b'M/W/F' and b'7:00am' in response.data


def test_edit_session(client, auth):
    auth.login()
    response = client.get('/sessions/1/edit')
    assert b'Edit Session' in response.data

    response = client.post('/sessions/1/edit', data={
        'session_days': 'S/Su',
        'session_time': '3:00pm'})

    assert '/sessions' in response.headers['Location']
