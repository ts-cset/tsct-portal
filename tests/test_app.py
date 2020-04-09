from portal import create_app


def test_config(monkeypatch):
    # Default config
    assert not create_app().testing

    # Test config
    assert create_app({'TESTING': True}).testing

    # Prod config
    monkeypatch.setenv('DATABASE_URL', "pretend this is on heroku...")
    assert "heroku" in create_app().config['DB_URL']
    assert "require" in create_app().config['DB_SSLMODE']


def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<p>Welcome to the TSCT Portal</p>' in response.data

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

def test_view_course(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses')
    assert b'101' in response.data
    assert b'Web Design' in response.data
    assert b'CSET' in response.data
    assert b'301' in response.data
    assert b'Public Speaking' in response.data
    assert b'GENEDS' in response.data

def test_create_course(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/create-course')
    response = client.post(
        '/portal/create-course', data={'course_number': '102', 'name':'CSET1', 'description':'class', 'credits':'9'}
    )
    response = client.get('/portal/courses')
    assert b'101' in response.data
    assert b'CSET1' in response.data
    assert b'CSET' in response.data


def test_update_course(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/create-course')
    response = client.post(
        '/portal/create-course', data={'course_number': '102', 'name':'CSET2', 'description':'class', 'credits':'10'}
    )
    response = client.get('/portal/courses')
    assert b'102' in response.data
    assert b'CSET2' in response.data
    assert b'CSET' in response.data
    response = client.post(
        '/portal/update-course/3', data={'course_number': '103', 'name':'CSET3', 'description':'class1', 'credits':'11'}
    )
    response = client.get('/portal/courses')
    assert b'102' not in response.data
    assert b'CSET2' not in response.data
    assert b'103' in response.data
    assert b'CSET3' in response.data
    assert b'CSET' in response.data
