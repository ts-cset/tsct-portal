import pytest


def test_home(client, auth):
    # log in as teacher and see teacher home Page
    # with list of courses
    auth.login()
    response = client.get('/home')
    assert b'Teacher Home Page' in response.data
    # course not owned by teacher
    assert b'ENG 101' in response.data
    # course owned by teacher
    assert b'METAL 155' in response.data


def test_my_courses(client, auth):
    # log in as teacher
    auth.login()
    # see only courses for this teacher
    response = client.get('/home/mycourses')
    # course not owned by teacher
    assert b'ENG 101' not in response.data
    # course owned by teacher
    assert b'METAL 155' in response.data
