import pytest

def test_submission_list(client):
    """Tests that adding a grade to a student's assignment submission works"""

    response = client.get('/course/180/session/2/assignments/1/submissions')

    assert response.status_code == 302

    with client:

        client.post('/login', data={'email': 'teacher2@stevenscollege.edu', 'password': 'PASSWORD'})

        response = client.get('/course/216/session/1/assignments/2/submissions')

        response.status_code == 200
        assert b'Marisa Kirisame' in response.data
        assert b'bob phillp' in response.data

def test_add_grade(client):

    with client:

        client.post('/login', data={'email': 'teacher2@stevenscollege.edu', 'password': 'PASSWORD'})

        response = client.get('/course/216/session/1/assignments/2/submissions/1')
        assert b'Enter feedback' in response.data

        response = client.post('/course/216/session/1/assignments/2/submissions/1',
            data={ 'grade': 25, 'feedback': 'good' })

        assert b'25' in response.data
        assert b'good' in response.data


@pytest.mark.parametrize(('email', 'password', 'route', 'error'), (
    ('teacher@stevenscollege.edu', 'qwerty', '2/submissions', 403),
    ('teacher@stevenscollege.edu', 'qwerty', '2/submissions/1', 403),
    ('student@stevenscollege.edu', 'asdfgh', '2/submissions', 403),
    ('student@stevenscollege.edu', 'asdfgh', '2/submissions/1', 403),
    ('teacher2@stevenscollege.edu', 'PASSWORD', '2/submissions/99', 404),
    ('teacher2@stevenscollege.edu', 'PASSWORD', '99/submissions/99', 404),
    ('teacher2@stevenscollege.edu', 'PASSWORD', '1/submissions/1', 403)
))
def test_submission_error_codes(client, email, password, route, error):

    with client:

        client.post('/login', data={'email': email, 'password': password})

        response = client.get(f'/course/216/session/1/assignments/{route}')

        assert response.status_code == error
