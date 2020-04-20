import pytest
import psycopg2

def test_create_course(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/create')
    assert b'Create New Course' in response.data
    # filling the form and Submit it
    response = client.post('/create', data = {
    'majors': 'BUSA',
    'new_course': 'math12222',
    'course_description': 'Enter description here'})
    # if it work redirect to the Home
    assert '/home' in response.headers['Location']
    response = client.get('/home')
    assert b'math12222'in response.data

def test_edit(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/3/edit')
    assert b'Edit Courses' in response.data
    assert b'CSET 180' in response.data
    # update the form the form and Submit it

    response = client.post('/3/edit', data = {
    'new_course': 'CSET 180',
    'course_description': 'This damn software project Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper quam et quam fringilla feugiat. Donec at risus efficitur, vehicula risus et, tempor nibh. Vivamus vitae porttitor metus, ac venenatis quam. Pellentesque porttitor malesuada orci iaculis condimentum. Vestibulum sodales, purus sit amet ultricies luctus, leo arcu mattis dui, at ultrices tortor eros sit amet lorem. Duis quis metus fringilla neque ornare ornare. Sed commodo sit amet elit et dictum. Nulla eget mattis ligula. Nulla sodales enim nec leo eleifend, et feugiat felis fermentum. Cras aliquet a magna ac pellentesque. Nulla ultrices bibendum dui tristique facilisis. Nam pellentesque lobortis ultricies. In id pretium quam. Sed facilisis lacinia lectus at tristique.'})
    # redirect to home
    assert '/home' in response.headers['Location']
    response = client.get('/home')
    assert b'CSET 180'in response.data
def test_delete(client, auth):
    # login to the page
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/home'

def test_view(client, auth):
    # login to the page
    auth.login()
    #get the course by clicking the view button
    response = client.post('/2/view')
    assert b'Course Information' in response.data
