import pytest

from portal.db import get_db

# get assignments that are assigned to the student
def test_view_assignments(app, client, auth):
    with app.app_context():
        db = get_db()

        cur = db.cursor()
        # login as student
        auth.login()

        # get it
        response = client.get('/assignments?course_id=1&section=A')
        assert b'homework' in response.data
        assert b'application' in response.data


# see all assignments of a session
def test_view_session_assignments(app, client, auth):
    with app.app_context():
        db = get_db()

        cur = db.cursor()
        # login as teacher
        auth.teacher_login()

        # get the assignments in the session
        response = client.get('/assignments?course_id=1&section=A')
        assert b'application' in response.data


def test_create_assignment(app, client, auth):
    with app.app_context():
        db = get_db()

        cur = db.cursor()
        # login as teacher
        auth.teacher_login()

        # create a new software project section A assignment
        client.post('/createassignment?course_id=1&section=A', data={
            'name': 'top ten review', 'type': 'essay', 'points': '100', 'duedate': '01/10/2020'})

        response = client.get('/assignments?course_id=1&section=A')
        assert b'top ten review' in response.data
