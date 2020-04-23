from portal import create_app

def test_grade_submission(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/assignments/1/1/grade-assignment/1', data={'points': '4.5'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Grade: A-' in response.data
    assert b'Points: 4.5' in response.data

def test_view_submission_grade_student(client):
    test_grade_submission(client)
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Grade: A-' in response.data
    assert b'Points: 4.5' in response.data
