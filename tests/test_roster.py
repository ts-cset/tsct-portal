import pytest

def test_roster_page(client):

    with client:
        client.post('/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

        response = client.get('/courses/180/sessions/2/roster')
        assert response.status_code == 200
        assert b'Software Project 2 CSET-180-A Roster' in response.data

def test_edit_roster(client):

    with client:
        client.post('/login', data={'email': 'teacher@stevenscollege.edu', 'password': 'qwerty'})

        #Check that a student appears in the roster list after being added
        response = client.post('/courses/180/sessions/2/roster', data={'email': 'student@stevenscollege.edu'})
        assert b'bob phillp' in response.data

@pytest.mark.parametrize(('email', 'message'), (
    ('incorrect@email.com', b'No student found'),
    ('teacher@stevenscollege.edu', b'zach fedor is not a student'),
    ('student2@stevenscollege.edu', b'Marisa Kirisame is already enrolled in this session')
))
def test_roster_validation(client, email, message):
    #Checks that the correct error message displays for invalid user additions
    with client:
        #First log in as the teacher so that the roster can be updated
        client.post('/login', data={'email': 'teacher2@stevenscollege.edu', 'password': 'PASSWORD'})

        response = client.post('/courses/216/sessions/1/roster', data={'email': email })

        assert message in response.data
