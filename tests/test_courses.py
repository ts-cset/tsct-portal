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

        cur.execute(
            "SELECT * FROM users WHERE email = 'teacher@stevenscollege.edu';"
            )
        user = cur.fetchone()
        with client.session_transaction() as sess: # stores teacher on the session
            sess['user'] = user

        # post it
        response = client.post('/createcourse', data={'cour_maj': 'CSET', 'cour_name': 'test', 'cour_num': 100, 'cour_cred': 3})
        # check the db and see if that course exists now
        cur.execute("SELECT * FROM courses WHERE name = 'test';")

        check = cur.fetchone()

        assert check

def test_edit_course(app, client):
    with app.app_context():
        db = get_db()

        cur = db.cursor()
        # post it again
        response = client.post('/1/editcourse', data={'cour_name': 'This is a test', 'cour_num': 111, 'cour_maj': 'CSET', 'cour_cred': 1, 'cour_desc': 'test'})
        # check if it's been updated
        cur.execute("SELECT * FROM courses WHERE credits = 1")
        check = cur.fetchone()

        assert check
