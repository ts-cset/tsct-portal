import pytest


def test_view_sessions(clent, auth):
    # getting the form as a logged in users
    auth.login()
    response = client.get('/sessions')
    assert b'Sessions' in response.data


def test_create_session(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/sessions/create')
    assert b'Add Session to Course :' in response.data

    response = client.post('/sessions/create', data={
        'courses': 'ENG 101',
        'days': 'M/W/F',
        'class_time': '7:00am'})

    assert '/sessions' in response.headers['Location']
    response = client.get('/sessions')
    assert b'M/W/F' and b'7:00am' in response.data
