from portal import create_app

def test_gradebook(client):
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/gradebook/')
    assert b'CSET 101-Web Design' in response.data
    assert b'43784 F' in response.data

def test_gradebook_student(client):
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/gradebook/')
    assert b'CSET 101-Web Design' in response.data
    assert b'43784 F' in response.data
    assert b'GENEDS 301-Public Speaking' not in response.data
