import pytest
from app.models.Product import Product

def test_get_all_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_product(client):
    response = client.post('/admin/products', json={
        "name": "Cat Food",
        "description": "Healthy cat food",
        "price": 15.0,
        "category": "Food",
        "stock_quantity": 100
    }, headers={"Authorization": "Bearer admin_token"})
    assert response.status_code == 201
    assert response.json['message'] == 'Product created successfully'