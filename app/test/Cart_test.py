import pytest
from app import db
from app.models.User import User
from app.models.Product import Product
from app.models.Order import Order

@pytest.fixture
def admin_user():
    admin = User(username="admin", email="admin@example.com", role="Admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    return admin

def test_get_all_users(client, admin_user):
    response = client.get('/admin/users', headers={"Authorization": "Bearer admin_token"})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_all_orders(client, admin_user):
    response = client.get('/admin/orders', headers={"Authorization": "Bearer admin_token"})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_stock(client, admin_user):
    product = Product(name="Dog Food", price=20.0, stock_quantity=10, category="Food")
    db.session.add(product)
    db.session.commit()

    response = client.put(
        f'/admin/products/{product.id}/stock',
        json={"stock_quantity": 50},
        headers={"Authorization": "Bearer admin_token"}
    )
    assert response.status_code == 200
    assert response.json['message'] == 'Stock updated successfully'