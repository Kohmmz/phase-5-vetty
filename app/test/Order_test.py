import pytest
from app.models.Order import Order
from app import db

def test_get_orders(client):
    response = client.get('/orders', headers={"Authorization": "Bearer user_token"})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_order(client):
    response = client.post('/orders', json={
        "items": [{"product_id": 1, "quantity": 2, "unit_price": 10.0}]
    }, headers={"Authorization": "Bearer user_token"})
    assert response.status_code == 201
    assert 'order_id' in response.json

def test_update_order_status(client):
    order = Order(user_id=1, total_price=100.0, status="pending")
    db.session.add(order)
    db.session.commit()

    response = client.put(
        f'/orders/{order.id}/status',
        json={"status": "completed"},
        headers={"Authorization": "Bearer admin_token"}
    )
    assert response.status_code == 200
    assert response.json['message'] == 'Order status updated successfully'