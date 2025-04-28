from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Route: Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200

# Route: Get single user by ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user), 200

# Route: Create (Signup) user
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validate data
    try:
        user_data = user_schema.load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Hash the password manually before saving
    hashed_password = generate_password_hash(data['password_hash'])

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        role=data.get('role', 'User')  # Default to 'User' if role not provided
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201

# Route: Update user
@user_bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    if 'password_hash' in data:
        user.password_hash = generate_password_hash(data['password_hash'])
    
    user.role = data.get('role', user.role)

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

# Route: Delete user
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
