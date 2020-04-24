import pytest

def test_student_classes(client , auth):
    auth.student_login()
    response = client.get('/student')
    assert b'Student Homepage' and b'METAL 255' in response.data
