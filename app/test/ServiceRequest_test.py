import pytest
from app.models.Service_request import ServiceRequest

def test_create_service_request(client):
    response = client.post('/service-requests', json={
        "user_id": 1,
        "service_id": 1,
        "appointment_time": "2025-05-01T10:00:00"
    }, headers={"Authorization": "Bearer user_token"})
    assert response.status_code == 201
    assert response.json['message'] == 'Service request created successfully'

def test_get_all_service_requests(client):
    response = client.get('/service-requests', headers={"Authorization": "Bearer admin_token"})
    assert response.status_code == 200
    assert isinstance(response.json, list)