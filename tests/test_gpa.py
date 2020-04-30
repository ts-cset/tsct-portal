import pytest

def test_view(client, auth):
    #this test if the user gets the right data
    auth.login()
    response = client.get('/course/2/session/2/gpa')
    assert b'Test Student' in response.data
