import pytest
from app import db
from app.models.Payment import Payment
from app.models.User import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def user_token():
    """
    Fixture to create a test user and generate a valid JWT token.
    """
    user = User(username="testuser", email="testuser@example.com", role="User")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return create_access_token(identity={"id": user.id, "role": user.role})

def test_create_payment(client, user_token):
    """
    Test creating a payment.
    """
    response = client.post('/payments', json={
        "order_id": 1,
        "payment_method": "credit_card",
        "amount": 100.0
    }, headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 201
    assert 'payment_id' in response.json

def test_get_payment(client, user_token):
    """
    Test retrieving a payment by ID.
    """
    payment = Payment(order_id=1, payment_method="credit_card", amount=100.0, status="paid")
    db.session.add(payment)
    db.session.commit()

    response = client.get(f'/payments/{payment.id}', headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id'] == payment.id