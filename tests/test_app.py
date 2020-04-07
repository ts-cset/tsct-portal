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
    assert b'<form>' in response.data


def test_login(client):
    assert client.get('/').status_code == 200
    response = client.post(
        '/', data={'email': "student@stevenscollege.edu", 'password': "pbkdf2:sha256:150000$bhcUxUAk$b08d717a84c93c4d09afe712f0d781b216e5b77a27b9becbf4d535fde22d0e97"})
    assert response.headers['Location'] == 'http://localhost/home'
