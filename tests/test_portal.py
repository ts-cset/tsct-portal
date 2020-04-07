from portal import create_app
import pytest


def test_config(monkeypatch):
    # Default config
    assert not create_app().testing

    # Test config
    assert create_app({'TESTING': True}).testing

    # Prod config
    monkeypatch.setenv('DATABASE_URL', "pretend this is on heroku...")
    assert "heroku" in create_app().config['DB_URL']
    assert "require" in create_app().config['DB_SSLMODE']


def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form>' in response.data


def test_edit(client):
    response = client.get('/courseManagement')
    assert b'<h2>Course Management<h2>' in response.data
    assert b'Edit' in response.data
    assert b'Info' in response.data
    assert b'+' in response.data


def test_create_course(client):
    response = client.get('/courseCreate')
    assert b'+' in response.data
    assert response.status_code() == 200 in response.data


def test_info_course(client):
    response = client.get('/courseInfo<ID>')
    assert b'Course Information on' in response.data
    assert b'Back' in response.data
