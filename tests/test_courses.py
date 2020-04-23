import pytest

from portal.db import get_db

def test_course_page(client, auth):
    auth.teacher_login()

    response = client.get('/courses')

    assert b'Software Project II' in response.data

def test_create_course(app, client, auth):
    with app.app_context(): # allows DB queries to happen
        db = get_db()

        cur = db.cursor()

        auth.teacher_login()

        # post it
        response = client.post('/createcourse', data={'cour_maj': 'CSET', 'cour_name': 'test course', 'cour_num': 100, 'cour_desc': 'test description', 'cour_cred': 3})
        # check the db and see if that course exists now
        cur.execute("SELECT * FROM courses WHERE name = 'test course';")

        check = cur.fetchone()

        assert check['description'] == 'test description'
        assert check['name'] == 'test course'
        assert check['num'] == 100

        # check if it exists in that teacher's courses page
        courses_resp = client.get('/courses')

        assert b'test course' in courses_resp.data

def test_edit_course(app, client, auth):
    with app.app_context():
        db = get_db()

        cur = db.cursor()

        auth.teacher_login()
        # post it again
        response = client.post('/1/editcourse', data={'cour_name': 'This is a test', 'cour_num': 111, 'cour_maj': 'CSET', 'cour_cred': 1, 'cour_desc': 'test description'})
        # check if it's been updated
        cur.execute("SELECT * FROM courses WHERE credits = 1")
        check = cur.fetchone()

        assert check['name'] == 'This is a test'
        assert check['credits'] == 1
        assert check['description'] == 'test description'

        # check if the change happened in that teacher's courses page
        courses_resp = client.get('/courses')

        assert b'This is a test' in courses_resp.data
def test_delete_course(app, client, auth):
    with app.app_context():
        db = get_db()

        cur = db.cursor()

        auth.teacher_login()

        response = client.post('/deletecourse', data={'course_to_delete': 4})
        cur.execute("SELECT * FROM courses WHERE name = 'Security and Ethics';")
        check = cur.fetchone()

        assert check is None
def test_course_view(app, client, auth):
    with app.app_context():
        db = get_db()

        cur = db.cursor()

        auth.teacher_login()

        response = client.get('/1/viewcourse')

        assert b'Software Project II' in response.data
        assert b'blaaah' in response.data
