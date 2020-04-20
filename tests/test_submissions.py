from portal import create_app

def test_view_submission(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Your submission' in response.data
    assert b'Answer: None' in response.data

def test_submit_submission(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.post(
        '/portal/assignments/1/submit-assignment', data={'answer':'Work'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Your submission' in response.data
    assert b'Answer: Work' in response.data

def test_view_submission_teacher(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Submissions' in response.data
    assert b'Student: 43784' in response.data
    assert b'Answer: None' in response.data
