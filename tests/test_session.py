import pytest


def test_view_sessions(client, auth):
    # getting the form as a logged in users,
    # reguarless if the user owns the course or not
    auth.login()
    response = client.get('/1/sessions')
    assert b'Current Sessions' and b'ENG 101' in response.data


def test_create_session(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/sessions/create')
    assert b'Add Session to Course :' in response.data
    # creating a new session for the course the teacher owns
    response = client.post('/sessions/create', data={
        'courses': 'ENG 201',
        'session_days': 'M/W/F',
        'class_time': '7:00am',
        'location': 'Main Campus'})
    # return to view list of sessions
    assert '5/sessions' in response.headers['Location']
    response = client.get('5/sessions')
    # make sure the new session shows up
    assert b'M/W/F' and b'07:00:00' in response.data


def test_edit_session(client, auth):
    # get to edit session as a teacher who owns the course
    auth.login()
    response = client.get('/sessions/2/edit')
    assert b'Edit Session' in response.data
    # editing session information for that session of that course
    response = client.post('/sessions/2/edit?course_id=2', data={
        'session_days': 'S/Su',
        'session_time': '7:00am',
        'location': 'Branch Campus'})
    # return to view of list of sessions
    assert '/2/sessions' in response.headers['Location']
    response = client.get('/2/sessions')
    # make sure new information is displayed for that session
    assert b'Current Sessions' in response.data
    assert b'S/Su' and b'07:00:00' in response.data


def test_get_session_edit(client, auth):
    # login as a teacher who does not own the course
    auth.login()
    # attempt to go to the edit page of a session of that course
    response = client.get('/sessions/6/edit?course_id=1')
    # make sure the abort message displays
    assert b'Bad Request' in response.data


# def test_delete_session(client, auth):
#     # login as a teacher who does not own the course/session
#     auth.login()
#     # attempt to delete a session not owned by user
#     response = client.get('/sessions/6/delete')
#     # make sure system aborts attempt
#     assert b'Bad Request' in response.data
