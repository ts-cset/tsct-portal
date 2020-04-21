import pytest

def test_create_assignment(client, auth):
    auth.login()
    #check the main assignment page works
    response = client.get('/2/assignments')
    assert b'Assignments' in response.data
    #check the create page works
    response = client.get('/2/create_assignment')
    assert b'Create Assignment' in response.data
    response = client.post('/2/create_assignment', data={
    'name': 'Magic',
    'description': 'It is leviOsa not LevioSA',
    'date': '2020-05-25'})
    assert '/2/assignments' in response.headers['location']

def test_edit_assignment(client, auth):
    auth.login()
    #Make sure the link to the edit works
    response = client.get('/3/edit-assignment')
    assert b'Edit your assignment' in response.data
    #Edit some data with other data
    response = client.post('/3/edit-assignment', data={
    'name': 'Magic2',
    'description': 'Who is this?',
    'date': '2020-05-25'})
    assert '/2/assignments' in response.headers['Location']
    response = client.get('/2/assignments')
    assert b'Magic2' in response.data

# def test_delete_assignment(client, auth):
#     auth.login()
#     response = client.post('/3/delete')
#     assert '/2/assignments' in response.headers['Location']
#     #failed delete
#     response = client.get('/6/delete_assignments')
#     assert b'Method Not Allowed' in response.data
