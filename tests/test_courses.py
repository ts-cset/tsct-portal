import pytest

from portal.db import get_db

def test_create_course(app, client):
    with app.app_context(): # allows DB queries to happen
        db = get_db()

        cur = db.cursor()
        # post it
        response = client.post('/createcourse', data={'coursenumber': 100, 'major': 'CSET', 'coursename': 'test'})
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
