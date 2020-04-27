import pytest


def test_view_sessions(client, auth):
    auth.login()
    response = client.get('/course/1/sessions')
    assert b'Current Sessions' in response.data
    assert b'ENG 101' in response.data
    # make sure teacher who doesn't own course cant see add session button
    assert b'add session' not in response.data


def test_create_session(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/course/2/session_create')
    assert b'Add Session to Course :' in response.data
    # creating a new session for the course the teacher owns
    response = client.post('/course/2/session_create', data={
        'session_days': 'M/W/F',
        'class_time': '7:00am',
        'location': 'Main Campus'})
    # return to view list of sessions
    assert 'course/2/sessions' in response.headers['Location']
    response = client.get('course/2/sessions')
    # make sure the new session shows up
    assert b'M/W/F' in response.data
    assert b'07:00:00' in response.data


def test_edit_session(client, auth):
    # get to edit session as a teacher who owns the course
    auth.login()
    response = client.get('/course/2/sessions/2/edit')
    assert b'Edit Session' in response.data
    # editing session information for that session of that course
    response = client.post('/course/2/sessions/2/edit', data={
        'session_days': 'S/Su',
        'session_time': '7:00am',
        'location': 'Branch Campus'})
    # return to view of list of sessions
    assert '/course/2/sessions' in response.headers['Location']
    response = client.get('/course/2/sessions')
    # make sure new information is displayed for that session
    assert b'METAL 155' in response.data
    assert b'S/Su' in response.data
    assert b'07:00:00' in response.data


def test_get_session_edit(client, auth):
    # login as a teacher who does not own the course
    auth.login()
    # attempt to go to the edit page of a session of that course
    response = client.get('/course/1/sessions/6/edit')
    # make sure the abort message displays
    assert b'Bad Request' in response.data


def test_delete_session(client, auth):
    # login as a teacher who does not own the course/session
    auth.login()
    # attempt to delete a session not owned by user
    response = client.post('/course/1/sessions/6/delete')
    # make sure system aborts attempt
    assert b'Bad Request' in response.data

    response = client.post('/course/2/sessions/2/delete')
    assert response.headers['Location'] == 'http://localhost/course/2/sessions'
    # make sure the course was deleted
    assert b'T/Th' not in response.data


def test_my_sessions(client, auth):
    # login as a teacher
    auth.login()
    # view the my sessions page
    response = client.get('/home/my_sessions')
    # make sure all the teachers current course sessions are listed
    assert b'METAL 155' in response.data
    assert b'CSET 180' in response.data
    assert b'DRAW 201' in response.data
    assert b'ENG 101'not in response.data
    # ensure the teacher os able to delete a session from this page
    response = client.post('/home/my_sessions/2/delete')
    assert response.headers['Location'] == 'http://localhost/home/my_sessions'
