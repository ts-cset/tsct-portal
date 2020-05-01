from portal import create_app

def test_grade_submission(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/assignments/1/1/grade-assignment/1', data={'points': '4.0', 'feedback': 'Good Job!'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Grade: B-' in response.data
    assert b'Points: 4.0' in response.data
    assert b'Good Job!' in respons.data

def test_view_submission_grade_student(client):
    test_grade_submission(client)
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Grade: B-' in response.data
    assert b'Points: 4.0' in response.data
    assert b'Good Job!' in respons.data
