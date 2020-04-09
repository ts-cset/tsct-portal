import pytest
from flask import g, session


def test_login(client):

    assert client.get('/').status_code == 302

    response = client.post('/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['email'] == 'teacher@stevenscollege.edu'


@pytest.mark.parametrize(('email', 'password', 'error'), (
    ('student@stevenscollege.edu', 'qwerty', b'Incorrect email or password'),
    ('teacher@stevens.college.edu', 'asdfgh', b'Incorrect email or password'),
    ('nonsense', 'not_a_correct_password', b'Incorrect email or password'),
    ('student@stevenscollege.edu', '', b'Enter a password'),
    ('', 'asdfgh', b'Enter an email')
))
def test_login_validation(client, email, password, error):

    response = client.post('/login', data={'email': email, 'password': password})

    assert error in response.data


def test_logout(client):

    client.post('/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

    with client:
        client.get('/logout')
        client.get('/')
        assert 'user_id' not in session
        assert g.user is None
