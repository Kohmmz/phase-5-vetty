import pytest
from app import create_app, db
from app.models.User import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def test_client():
    """
    Fixture to create a test client for the Flask application.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory SQLite for testing
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def admin_token(test_client):
    """
    Fixture to create an admin user and generate a valid JWT token.
    """
    admin = User(username="admin", email="admin@example.com", role="Admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    return create_access_token(identity={"id": admin.id, "role": admin.role})

@pytest.fixture
def user_token(test_client):
    """
    Fixture to create a test user and generate a valid JWT token.
    """
    user = User(username="testuser", email="testuser@example.com", role="User")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return create_access_token(identity={"id": user.id, "role": user.role})