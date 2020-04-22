import pytest

def test_add_grade(client):
    """Tests that adding a grade to a student's assignment submission works"""

    response = client.get('/course/180/session/2/assignments/1/submissions')

    assert response.status_code == 302

    with client:

        client.post('/login', data={'email': 'teacher2@stevenscollege.edu', 'password': 'PASSWORD'})

        response = client.get('/course/216/session/1/assignments/2/submissions')

        response.status_code == 200
        assert b'Marisa Kirisame' in response.data
        assert b'bob phillp' in response.data

        response = client.get('/course/216/session/1/assignments/2/submissions/1')
        assert b'Insert feedback' in response.data

        response = client.post('/course/216/session/1/assignments/2/submissions/1',
            data={ 'grade': 25, 'feedback': 'good' })

        assert b'25' in response.data
        assert b'good' in response.data
