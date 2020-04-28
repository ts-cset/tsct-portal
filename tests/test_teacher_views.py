import pytest
from portal.student_views import view_schedule
from .test_courses import login, logout

def test_all_grades(client):
    # Make sure anonymous users cannot access
    assert client.get('/course/180/session/2/allGrades') == 403
    # Login
    rv = login(client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data
    # Make sure teacher can access
    assert client.get('/course/180/session/2/allGrades') == 200

    response = client.get('/course/180/session/2/allGrades')
    # Making sure students grades are displaying
    assert 'bob phillp' in response.data
    assert 'A' in response.data
    # Logout
    rv = logout(client)
    assert b'TSCT Portal Login' in rv.data
