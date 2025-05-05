from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role}, expires_delta=timedelta(hours=1))
        return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/auto-login', methods=['GET'])
@jwt_required()
def auto_login():
    identity = get_jwt_identity()
    return jsonify({'user': identity}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logout handled client-side by removing token'}), 200

# Current User
@auth_bp.route('/current_user', methods=['GET'])
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()
    # Extract the user ID if it's in a dictionary format
    if isinstance(current_user_id, dict) and 'id' in current_user_id:
        current_user_id = current_user_id['id']
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    user_data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'role': user.role
    }

    return jsonify(user_data)
