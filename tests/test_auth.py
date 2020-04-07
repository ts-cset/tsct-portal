import pytest
from flask import g, session
from portal.db import get_db

def test_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    #with client:
        #client.get('/teacher-page')
        #assert session['user_id'] == 1
        #assert g.user['email'] == 'teacher@stevenscollege.edu'

@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password.'),
    ('test', 'a', b'Incorrect username or password.'),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
