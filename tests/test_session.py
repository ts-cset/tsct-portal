import pytest


def test_view_sessions(client, auth):
    auth.login()
    response = client.get('/2/sessions')
    assert b'Sessions' in response.data
