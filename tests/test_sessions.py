from portal import create_app

def test_create_session(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.post(
        '/portal/sessions/1/create-session', data={'name': 'A', 'times':'Monday', 'students':43784}
    )
