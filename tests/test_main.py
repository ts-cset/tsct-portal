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


def test_teacher_assignment_grades(client, auth):
    # log in as a teacher
    auth.login()
    #see grades for an assignments
    response = client.get('/course/2/session/2/assignments/3/grades')
    #make sure the page shows up
    assert b'Assignment: 3' in response.data
    #make sure the data was returned
    assert b'<td>Test Student</td>' in response.data

def test_input_grade(client, auth):
    #log in as a teacher
    auth.login()
    #see grade input for correct assignment
    response =  client.get('/course/2/session/2/assignments/3/input-grade/12')
    assert b'Assignment: 3' in response.data
    #make a grade input - redirected to correct place with correct data
    response = client.post('/course/2/session/2/assignments/3/input-grade/12', data={
        'feedback': 'Very good grade!',
        'grade_input': 5
        })
    #make sure redirecting to correct place
    assert '/3/grades' in response.headers['Location']
    response =  client.get('/course/2/session/2/assignments/3/grades')
    #make sure new data is updated on the page after submission
    assert b'<td>5.00</td>' in response.data
