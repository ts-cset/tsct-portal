import pytest

def test_roster_page(client):

    response = client.get('/roster')
    assert response.status_code == 200
    assert b'CSET 180 A Roster' in response.data

def test_edit_roster(client):

    #Check that a student appears in the roster list after being added
    response = client.post('/roster', data={'email': 'student@stevenscollege.edu'})
    assert b'student@stevenscollege.edu' in response.data

@pytest.mark.parametrize(('email', 'message'), (
    ('incorrect@email.com', b'No student found'),
    ('teacher@stevenscollege.edu', b'Teacher is not a student'),
    ('student2@stevenscollege.edu', b'Student2 is already registered')
))
def test_roster_validation(client, email, message):

    response = client.post('/roster', data={'email': email })

    assert message in resposne.data
