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
    response = client.get('/auth/login?email=teacher%40stevenscollege.edu&password=qwerty')
    response = client.get('/portal/userpage')
    assert b'<p>You are logged in</p>' in response.data
    assert b'Log In' not in response.data
    assert b'Log Out' in response.data
    assert b'User Page' in response.data

def test_logout(client):
    response = client.get('/auth/login')
    response = client.get('/auth/login?email=teacher%40stevenscollege.edu&password=qwerty')
    response = client.get('/portal/userpage')
    response = client.get('/auth/logout')
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Log Out' not in response.data
    assert b'User Page' not in response.data
