import pytest


def test_home(client, auth):
    auth.login()
    response = client.get('/home')
    assert b'Teacher Home Page' in response.data
    assert b'ENG 101' in response.data
