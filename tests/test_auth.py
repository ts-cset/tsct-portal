from portal import create_app

def test_login(client):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Log Out' not in response.data
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    assert b'teacher@stevenscollege.edu' in response.data
    assert b'Log In' not in response.data
    assert b'Log Out' in response.data
    assert b'User Page' in response.data
    assert b'Courses' in response.data
    response = client.get('/auth/logout')
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/userpage')
    assert b'student@stevenscollege.edu' in response.data
    assert b'Log In' not in response.data
    assert b'Log Out' in response.data
    assert b'User Page' in response.data
    assert b'Courses' in response.data

def test_login_error(client):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Log Out' not in response.data
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'yes'}
    )
    assert b'Log In' in response.data
    assert b'Incorrect email or password' in response.data
    assert b'Log Out' not in response.data
    assert b'User Page' not in response.data
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'yes'}
    )
    assert b'Log In' in response.data
    assert b'Incorrect email or password' in response.data
    assert b'Log Out' not in response.data
    assert b'User Page' not in response.data

def test_logout(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/auth/logout')
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Log Out' not in response.data
    assert b'User Page' not in response.data
