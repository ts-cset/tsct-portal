import pytest

def test_roster_page(client):

    response = client.get('/roster')
    assert response.status_code == 200
    assert b'CSET 180 A Roster' in response.data

def test_edit_roster(client):

    #Check that a student appears in the roster list after being added
    response = client.post('/roster', data={'email': 'student@stevenscollege.edu'})
    assert b'student@stevenscollege.edu' in response.data
