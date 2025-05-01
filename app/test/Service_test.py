import pytest
from app.models.Service import Service

def test_get_all_services(client):
    response = client.get('/services')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_service(client):
    response = client.post('/admin/services', json={
        "name": "Grooming",
        "description": "Pet grooming service",
        "price": 50.0
    }, headers={"Authorization": "Bearer admin_token"})
    assert response.status_code == 201
    assert response.json['message'] == 'Service created successfully'