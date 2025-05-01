import pytest
from app.models.User import User

def test_register_user(client):
    response = client.post('/auth/register', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert 'id' in response.json

def test_login_user(client):
    response = client.post('/auth/login', json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
