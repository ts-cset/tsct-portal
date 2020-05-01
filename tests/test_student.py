import pytest


def test_student_classes(client, auth):
    # login required
    auth.student_login()
    # get the page
    response = client.get('/student')
    # check the following data in page
    assert b'Student Homepage' in response.data
    assert b'METAL 255' in response.data


def test_student_grade(client, auth):
    # login required
    auth.student_login()
    # click the button to see the assignment grade
    response = client.get('/student/course/3/session/1/assignment/1/grade')
    # check the following data in page
    assert b'Assignment Grades' in response.data


def test_view_student_gradebook(client, auth):
    # login required
    auth.student_login()
    # click the button to see the  grade
    response = client.get('/student/gradebook')
    # check the following data in page
    assert b'Student Gradebook' in response.data
    assert b'All Student Courses' in response.data


def test_view_grades_by_course(client, auth):
    # login required
    auth.student_login()
    # click the button to see the  grade
    response = client.get('/student/gradebook/course/3/session/1')
    # check the following data in page
    assert b'Course Grade' in response.data
    assert b'Exam_1' in response.data
