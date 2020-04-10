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
    assert b'<p>You are logged in</p>' in response.data
    assert b'teacher@stevenscollege.edu' in response.data
    assert b'Log In' not in response.data
    assert b'Log Out' in response.data
    assert b'User Page' in response.data
    assert b'You are a teacher' in response.data
    response = client.get('/auth/logout')
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/userpage')
    assert b'<p>You are logged in</p>' in response.data
    assert b'student@stevenscollege.edu' in response.data
    assert b'Log In' not in response.data
    assert b'Log Out' in response.data
    assert b'User Page' in response.data
    assert b'You are a teacher' not in response.data

def test_login_fail(client):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Log Out' not in response.data
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'yes'}
    )
    assert b'Log In' in response.data
    assert b'Log Out' not in response.data
    assert b'User Page' not in response.data
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'yes'}
    )
    assert b'Log In' in response.data
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
    
