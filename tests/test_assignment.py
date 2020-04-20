from portal import create_app
import pytest

def test_create_assignment(client, auth):
    auth.login()
    #check the main assignment page works
    response = client.get('/1/assignments')
    assert b'Create new assignment for 1' in response.data
    #check the create page works
    response = client.get('/1/create_assignment')
    assert b'Save new assignment' in response.data
    response = client.post('/1/assignments', data={
    'name': 'Magic Class',
    'description': 'It is leviOsa not LevioSA',
    'due_date': '11/28/2001'
    })
    assert b'Create new assignment for 1' in response.data
    #check that the user must enter all fields before submitting
    #response = client.get('/1/create_assignment')
    #response = client.post('/1/assignments', data={
    #'name': 'Magic Class',
    #'description': '',
    #'due_date': '11/28/2001'
    #})
    #assert 'Description cannot be empty' in response.data
