from portal import create_app

def test_courses(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/')
    assert b'101' in response.data
    assert b'Web Design' in response.data
    assert b'CSET' in response.data
    assert b'301' in response.data
    assert b'Public Speaking' in response.data
    assert b'GENEDS' in response.data

def test_view_course(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/view-course/1')
    assert b'101' in response.data
    assert b'Web Design' in response.data
    assert b'CSET' in response.data
    assert b'Sessions' in response.data
    assert b'Name: A' in response.data
    assert b'Times: monday' in response.data
    assert b'301' not in response.data
    assert b'Public Speaking' not in response.data
    assert b'GENEDS' not in response.data

def test_courses_student(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/')
    assert b'101' in response.data
    assert b'Web Design' in response.data
    assert b'CSET' in response.data
    assert b'301' not in response.data
    assert b'Public Speaking' not in response.data
    assert b'GENEDS' not in response.data

def test_view_course_student(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'student@stevenscollege.edu', 'password':'asdfgh'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/view-course/1')
    assert b'101' in response.data
    assert b'Web Design' in response.data
    assert b'CSET' in response.data
    assert b'Sessions' in response.data
    assert b'Name: A' in response.data
    assert b'Times: monday' in response.data
    assert b'301' not in response.data
    assert b'Public Speaking' not in response.data
    assert b'GENEDS' not in response.data

def test_create_course(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/create-course')
    response = client.post(
        '/portal/courses/create-course', data={'course_number': '102', 'name':'Project', 'description':'class', 'credits':'9'}
    )
    response = client.get('/portal/courses/')
    assert b'102' in response.data
    assert b'Project' in response.data
    assert b'CSET' in response.data

def test_create_course_error(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/create-course')
    response = client.post(
        '/portal/courses/create-course', data={'course_number': '101', 'name':'Web Design', 'description':'class', 'credits':'9'}
    )
    assert b'That course already exists' in response.data

def test_update_course(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/create-course')
    response = client.post(
        '/portal/courses/create-course', data={'course_number': '102', 'name':'CSET2', 'description':'class', 'credits':'10'}
    )
    response = client.get('/portal/courses/')
    assert b'102' in response.data
    assert b'CSET2' in response.data
    assert b'CSET' in response.data
    response = client.post(
        '/portal/courses/update-course/3', data={'course_number': '103', 'name':'CSET3', 'description':'class1', 'credits':'11'}
    )
    response = client.get('/portal/courses/')
    assert b'102' not in response.data
    assert b'CSET2' not in response.data
    assert b'103' in response.data
    assert b'CSET3' in response.data
    assert b'CSET' in response.data

def test_update_course_fail(client):
    response = client.get('/auth/login')
    response = client.post(
        '/auth/login', data={'email': 'teacher@stevenscollege.edu', 'password':'qwerty'}
    )
    response = client.get('/portal/userpage')
    response = client.get('/portal/courses/create-course')
    response = client.post(
        '/portal/courses/create-course', data={'course_number': '102', 'name':'CSET2', 'description':'class', 'credits':'10'}
    )
    response = client.get('/portal/courses/')
    assert b'102' in response.data
    assert b'CSET2' in response.data
    assert b'CSET' in response.data
    response = client.post(
        '/portal/courses/update-course/3', data={'course_number': '101', 'name':'Web Design', 'description':'class', 'credits':'11'}
    )
    assert b'That course already exists' in response.data
