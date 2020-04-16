from flask import g, session, url_for
import pytest
from portal.db import get_db
from portal.auth import login, logout
import os
import tempfile

def test_assign_create(client):

    #test that assign_create exists
    assert client.get('/assign_create/180/20').status_code == 302


    rv = login(
        client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data

    #test getting the assign created
    assert client.get('/assign_create/180/20').status_code == 200
    #check response data for response assign create
    response == client.get('/assign_create/180/20')
    assert b'create assignment in software project 2-A' in response.data
    assert b'assignment name' in response.data
    #make post request to test functionality of test created
    #test redirection to assign manage
    response_2 = client.post('/assign_create/180/20', data={name: 'portal creation',
     description: 'testing_description', points: 100},follow_redirects = True)
    #in assign manage data make sure assign manage is there
    assert b'Assignments for software project 2-A' in response_2.data
    assert b'portal creation' in response_2.data


    rv = logout(client)
    assert b'TSCT Portal Login' in rv.data


@pytest.mark.parametrize(('name', 'description', 'points', 'error'),(
    ('testing exam', 'enter discription', '', b'points are required'),
    ('', 'enter description', '90', b'name is requred')
    ))

def test_create_errors(client,name,description,points,error):
    response = client.post('/assign_create/32/180/20', data={'name': name,
     'description': description, 'points': points},follow_redirects = True)
    assert error in response.data



def test_assign_manage(client):

    #test getting assignment manage
    assert client.get('/assign_manage/180/20').status_code == 302
    #can we login
    rv = login(
     client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data
     #can we access after login
    assert client.get('/assign_manage/180/20').status_code == 200
     #test data of the page
    response = client.get('/assign_manage/180/20')
    assert b'Assignments for software project 2' in response_2.data
    assert b'click plus symbol below to create assignment' in response_2.data
     #logout
    rv = logout(client)
    assert b'TSCT Portal Login' in rv.data

def test_assign_veiw(client):

    #test getting assign veiw
    assert client.get('/assign_veiw/32/180/20').status_code == 302
    #can login
    rv = login(
     client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data
    #can we access after login
    assert client.get('/assign_veiw/32/180/20').status_code == 200
    #check the veiw of page
    response = client.get('/assign_veiw/32/180/20')
    assert b'details of exam1' in response.data
    assert b'first exam of course' in response.data
    assert b'points out of 100' in response.data
    #logout
    rv = logout(client)
    assert b'TSCT Portal Login' in rv.data

def test_assign_edit(client):

    #test getting assignemnt edit
    assert client.get('/assign_edit/32/180/20').status_code == 302
    rv = login(
     client, 'teacher@stevenscollege.edu', 'qwerty')
    assert b'Logged in' in rv.data
    #test the assign edit after login
    assert client.get('/assign_edit/32/180/20').status_code == 200
    #get response data on page
    response = client.get('/assign_edit/32/180/20')
    #getting data on edit page
    assert b'name' in response.data
    assert b'description' in response.data
    assert b'points' in response.data
    #editing the page with request
    response_2 = client.post('/assign_edit/32/180/20', data={'edit_name': 'first portal creation',
     'edit_desc': 'first test', 'edit_points': 90},follow_redirects = True)
    assert b'Assignments for software project 2-A' in response.data
    assert b'first portal creation' in response.data
    #logout
    rv = logout(client)
    assert b'TSCT Portal Login' in rv.data


@pytest.mark.parametrize(('name', 'description', 'points', 'error'),(
    ('testing exam', 'enter discription', '', b'points are required'),
    ('', 'enter description', '90', b'name is requred')
    ))

def test_edit_errors(client,name,description,points,error):
    response = client.post('/assign_edit/32/180/20', data={'edit_name': name,
     'edit_desc': descrition, 'edit_points': points},follow_redirects = True)
    assert error in response.data
