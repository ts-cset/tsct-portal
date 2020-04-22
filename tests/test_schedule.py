import pytest
from portal.schedule import view_schedule
from .test_course_editor import login, logout

# I need to verify that there is a connection to the database
#
# For the render_template line, check for something that should always be on the
# schedule page, like "Schedule" or "Title", something like that
#

def test_schedule_view(client):
    assert client.get('/schedule').status_code == 302
    # login to check database
    rv = login(client, 'student@stevenscollege.edu', 'asdfgh')
    assert b'Logged in' in rv.data
    # go to schedule view to test data on page
    assert client.get('/schedule').status_code == 200
    response = client.get('/schedule')
    # test to see if mock data is on page, and see if the location/url is correct
    assert b'Teacher Name' in response.data
    assert b'Ms.Sullivan' in response.data
    # test logging out
    rv = logout(client)
    assert b'TSCT Portal Login' in rv.data
