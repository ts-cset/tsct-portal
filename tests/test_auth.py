import pytest
from flask import g, session


def test_login(client):

    assert client.get('/login').status_code == 200

    response = client.post('/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

    assert response.headers['Location'] == 'http://localhost/'

    with client.get('/'):

        assert session['user_id'] == 1
        assert g.user['email'] == 'teacher@stevenscollege.edu'


@pytest.mark.parametrize(('email', 'password'), (
    ('student@stevenscollege.edu', 'qwerty'),
    ('teacher@stevens.college.edu', 'asdfgh'),
    ('nonsense', 'not_a_correct_password')
))
def test_login_validation(client, email, password):

    response = client.post('/login', data={'email': email, 'password': password})

    assert b'Incorrect email or password' in response.data
