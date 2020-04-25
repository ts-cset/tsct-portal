import pytest

def test_view_roster(client, auth):
    # getting the form as a logged in users,
    # reguarless if the user owns the roster or not
    auth.login()
    response = client.get('/course/2/session/2/roster')
    assert b'Class Roster' and b'Test Student' in response.data

def test_roster_add(client, auth):
    auth.login()
    # post request to add to the roster as a loggedin user
    response = client.post('/course/2/session/2/roster', data={
    'sname':'Test Student 2',
    'rname':''})
    assert b'Test Student 2' in response.data

def test_roster_delete(client, auth):
    # posts a request to remove a student from the roster
    auth.login()
    response = client.post('/course/2/session/2/roster', data={
    'sname': '',
    'rname': 'Test Student'})
    assert b'  <li class="student-name">Test Student</li>' not in response.data
