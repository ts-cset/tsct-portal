from portal import create_app

def test_create_session(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/sessions/1/create-session', data={'name': 'B', 'times':'tuesday', 'students':43784}
    )
    response = client.get('/portal/courses/view-course/1')
    assert b'tuesday' in response.data
    assert b'B' in response.data

def test_create_session_error(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/sessions/1/create-session', data={'name': 'BB', 'times':'tuesday', 'students':43784}
    )
    assert b'There was a problem creating that session' in response.data
    response = client.post(
        '/portal/sessions/1/create-session', data={'name': 'A', 'times':'monday', 'students':43784}
    )
    assert b'That session already exists' in response.data

def test_view_session(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/sessions/1/view-session/1')
    assert b'Create Assignments' in response.data
    assert b'monday' in response.data
    assert b'A' in response.data
    assert b'43784' in response.data
    assert b'Assignment: Homework' in response.data
    assert b'Due: 2000-12-31' in response.data

def test_view_session_student(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/sessions/1/view-session/1')
    assert b'Create Assignments' not in response.data
    assert b'monday' in response.data
    assert b'A' in response.data
    assert b'43784' not in response.data
    assert b'Assignment: Homework' in response.data
    assert b'Due: 2000-12-31' in response.data
