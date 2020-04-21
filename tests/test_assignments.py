from portal import create_app

def test_create_assignment(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/assignments/1/create-assignment', data={'name': 'Quiz1', 'date':'2000-05-05', 'description':'Take this quiz','points':'5'}
    )
    response = client.get('/portal/sessions/1/view-session/1')
    assert b'Quiz1' in response.data
    assert b'2000-05-05' in response.data

def test_create_assignment_error(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.post(
        '/portal/assignments/1/create-assignment', data={'name': 'Quiz2', 'date':'2 days', 'description':'Take this quiz','points':'5'}
    )
    assert b'There was a problem creating that assignment' in response.data
    response = client.post(
        '/portal/assignments/1/create-assignment', data={'name': 'Homework', 'date':'2000-12-31', 'description':'homework','points':'5'}
    )
    assert b'That assignment already exists' in response.data

def test_view_assignment(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Homework' in response.data
    assert b'2000-12-31' in response.data
    assert b'homework' in response.data
    assert b'5' in response.data

def test_view_assignment_student(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/assignments/1/1/view-assignment/1')
    assert b'Homework' in response.data
    assert b'2000-12-31' in response.data
    assert b'homework' in response.data
    assert b'5' in response.data
