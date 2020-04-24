import pytest

def test_student_classes(client , auth):
    auth.student_login()
    response = client.get('/student')
    assert b'Student Homepage' in response.data
    assert b'METAL 255' in response.data
def test_student_grade(client , auth):
    auth.student_login()
    response = client.get('/student/course/3/session/1/assignment/1/grade')
    assert b'Assignment Grades' in response.data
def test_view_student_gradebook(client , auth):
    auth.student_login()
    response = client.get('/student/gradebook')
    assert b'Student Gradebook' in response.data
    assert b'All Student Courses' in response.data
def test_view_grades_by_course(client , auth):
    auth.student_login()
    response = client.get('/student/gradebook/course/3')
    assert b'Course Grades' in response.data
    assert b'CSET 180' in response.data
