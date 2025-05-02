from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app import db
from app.models.User import User
from app.schemas.User_schema import UserSchema
from app.utils.jwt_utils import generate_jwt_token
from app.utils.email_util import send_verification_email
import random

user_bp = Blueprint('user', __name__, url_prefix='/users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Temporary store for OTPs (use a database or cache in production)
otp_store = {}

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    try:
        user_schema.load(data, instance=user, partial=False)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    db.session.commit()
    return jsonify(user_schema.dump(user)), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204

@user_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = user_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    db.session.add(user)
    db.session.commit()

    # Generate OTP and send verification email
    otp = random.randint(100000, 999999)
    otp_store[user.email] = otp
    send_verification_email(user.email, otp)

    return jsonify({"message": "User created. Verification email sent."}), 201

@user_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if email in otp_store and otp_store[email] == otp:
        del otp_store[email]
        return jsonify({"message": "Email verified successfully."}), 200
    return jsonify({"error": "Invalid OTP or email."}), 400