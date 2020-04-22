import pytest

def test_view_roster(client, auth):
    # getting the form as a logged in users,
    # reguarless if the user owns the session or not
    auth.login()
    response = client.get('/course/2/session/2/roster')
    assert b'Class Roster' in response.data

def test_roster_add(client, auth):
    auth.login()
    response = client.post('/course/2/session/2/roster', data={
    'sname':'Test Student 2',
    'rname':''})
    assert b'Test Student 2' in response.data

def test_roster_delete(client, auth):
    auth.login()
    response = client.post('/course/2/session/2/roster', data={
    'sname': 'Test Student',
    'rname': ''})
    assert b'Test Student' in response.data
