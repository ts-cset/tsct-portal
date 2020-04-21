import pytest

from flask import session
from portal.db import get_db

def test_assignments_page(app, client, auth):
    with app.app_context(): #Allows queries to execute
        auth.login()

        response = client.get('/assignments')

    assert ('portal/home.html')
    assert ("portal/assignments.html")
    assert b'homework' in response.data
