from portal import create_app

def test_create_session(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/sessions/1/create-session', data={'name': 'A', 'times':'Monday', 'students':43784}
    )
    response = client.get('/portal/courses/view-course/1')
    assert b'Monday' in response.data
    assert b'A' in response.data

def test_view_session(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/sessions/1/create-session', data={'name': 'B', 'times':'Tuesday', 'students':43784}
    )
    response = client.get('/portal/sessions/1/view-session/1')
    assert b'Create Assignments' in response.data
    assert b'Tuesday' in response.data
    assert b'B' in response.data
    assert b'43784' in response.data
