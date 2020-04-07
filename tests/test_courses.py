import pytest
import psycopg2

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
