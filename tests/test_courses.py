import pytest

from flask import session
from portal.db import get_db

def test_course_page(app, client):
    with app.app_context():
        cur = get_db().cursor()

        cur.execute(
            "SELECT * FROM users WHERE email = 'teacher@stevenscollege.edu';"
            )
        user = cur.fetchone()
        with client.session_transaction() as sess: # stores teacher on the session
            sess['user'] = user

        response = client.get('/courses')

        assert response
        assert b'Software Project II' in response.data

def test_create_course(app, client):
    with app.app_context(): # allows DB queries to happen
        db = get_db()

        cur = db.cursor()
        # post it
        response = client.post('/courses/createcourse', data={'coursenumber': 100, 'major': 'CSET', 'coursename': 'test'})
        # check the db and see if that course exists now
        check = cur.execute("SELECT * FROM courses WHERE name = 'test';").fetchone()

        assert check

def test_edit_course(app, client):
    with app.app_context():
        db = get_db()

        cur = db.cursor()
        # post it again
        response = client.post('/editcourse', data={'credits': 14})
        # check if it's been updated
        check = cur.execute("SELECT * FROM courses WHERE credits = 14")

        assert check
