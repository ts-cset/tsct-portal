import pytest
from flask import g, session, url_for, request
from portal.db import get_db

def test_home(client, auth):
    # Attempt to visit page without logging in
    response = client.get('/teacher/home')
    # Non-authorized users should be redirected to login
    assert 'http://localhost/' == response.headers['Location']
    # Log in as a teacher
    auth.teacher_login()
    response = client.get('/teacher/home')
    # Logged-in teachers should not be redirected
    assert b'Manage Courses' in response.data

def test_courses(client, auth):
    auth.teacher_login()

    response = client.get('/teacher/courses')
    # Check that mock course exists
    assert b'Big Software Energy' in response.data

    # Attempt to delete mock course
    response = client.post(
        '/teacher/courses',
        data={'id':1}
    )

    # Check that mock course no longer exists
    assert b'Big Software Energy' not in response.data

    # Teachers shouldn't be able to delete courses that they don't own
    response = client.post(
        '/teacher/courses',
        data={'id': 4}
    )
    assert b'Something went wrong.' in response.data

def test_creation(client, auth):
    auth.teacher_login()
    #Makes sure that you can go to Class Creation
    assert client.get('/teacher/courses/create').status_code == 200
    #Fills out the form in Class Creation
    response = client.post(
        '/teacher/courses/create',
        data={'code': 180, 'name': 'Software Project II', 'major': 'CSET',
        'description': 'A basic computer course'}
    )
    #Asserts that it's switched over to the Course Selection
    assert 'http://localhost/teacher/courses' == response.headers['Location']

    # Teachers shouldn't be able to create courses with invalid data
    response = client.post(
        '/teacher/courses/create',
        data={'code': 'Not even a number', 'name': 'Software Project II', 'major': 'CSET',
        'description': 'A basic computer course'}
    )
    assert b'Something went wrong.' in response.data

def test_course_edit(client,auth,app):
    auth.teacher_login()
    #Get the elements of the edit page
    response = client.get('teacher/courses/1/edit')
    #Make sure the title 'Course-Edit' is inside.
    assert b'Edit Big Software Energy' in response.data
    #Using App context to execute commands, so that the database has a context to work off of.
    with app.app_context():
        #Post data to edit
        res = client.post(
            '/teacher/courses/1/edit',
            data={'code': 500, 'name': 'Ice-Cream', 'major': 'CSET',
            'description': 'A basic introduction to Ice-Cream'}
        )
        #Select data from DB
        with get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT * FROM courses
                    WHERE id = %s
                """,(1,))

                #Store all of it in results
                result = cur.fetchone()

                #Assert that the course name is the same as the course-name that was updated.
                assert result['course_name'] == 'Ice-Cream'

                #Assert that it returned to the courses page.
                assert res.headers['Location'] == 'http://localhost/teacher/courses'

    # Teachers should not be able to view the edit page for courses they do not own
    response = client.get('/teacher/courses/4/edit')
    assert 'http://localhost/teacher/courses' == response.headers['Location']

    # Teachers should not be able to post invalid data when editing a course
    response = client.post(
        '/teacher/courses/1/edit',
        data={'code': 500, 'name': 'Ice-Cream', 'major': 'TOOLONG',
        'description': 'A basic introduction to Ice-Cream'}
    )
    assert b'Something went wrong.' in response.data
