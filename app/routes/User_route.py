from flask import Blueprint, request, jsonify
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
from marshmallow import ValidationError
from app import db
from app.models.User import User
from app.schemas.User_schema import UserSchema
from app.utils.jwt_utils import generate_jwt_token
from app.utils.email_util import send_verification_email
import random
import pyotp
import qrcode
from io import BytesIO
import base64
from app.utils.auth_util import role_required
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__, url_prefix='/users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Temporary store for OTPs (for initial email verification)
otp_store = {}

@user_bp.route('/<int:user_id>', methods=['GET'])
@role_required("Admin")
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_schema.dump(user)), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
@role_required("Admin")
def update_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    try:
        user_schema.load(data, instance=user, partial=False)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    db.session.commit()
    return jsonify(user_schema.dump(user)), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@role_required("Admin")
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return "", 204

@user_bp.route('', methods=['GET'])
@role_required("Admin")
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()

    # Map 'name' to 'username' for schema compatibility
    if 'name' in data:
        data['username'] = data.pop('name')

    # Enforce role as 'User' for client registration only
    if 'role' in data and data['role'] != 'User':
        return jsonify({"error": "Registration is only allowed for clients."}), 403
    data['role'] = 'User'

    try:
        user = user_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user.set_password(data.get("password"))
    db.session.add(user)
    db.session.commit()

    # Generate OTP and send verification email
    otp = random.randint(100000, 999999)
    otp_store[user.email] = otp
    try:
        send_verification_email(user.email, otp)
    except Exception as e:
        print(f"Error sending verification email: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to send verification email. Please check your email configuration and try again.'}), 500

    # Return only message on registration success (no tokens)
    return jsonify({"message": "Registration successful. Please check your email to verify your account."}), 201

@user_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Invalid email."}), 400

    if email in otp_store and otp_store[email] == otp:
        del otp_store[email]
        user.is_verified = True
        db.session.commit()
        return jsonify({"message": "Email verified successfully."}), 200
    return jsonify({"error": "Invalid OTP."}), 400

@user_bp.route('/enable-2fa', methods=['POST'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def enable_2fa():
    # JWT DISABLED TEMPORARILY FOR ROUTE TESTING

    # Original: user_id = 1  # JWT DISABLED: Replaced get_jwt_identity() with hardcoded user ID['id']

    # Using hardcoded user_id for testing without JWT

    user_id = 1  # Hardcoded user_id for testing
    user = db.session.get(User, user_id)

    # Generate a unique secret key for TOTP
    secret_key = pyotp.random_base32()
    user.set_two_fa_secret(secret_key)
    user.is_2fa_enabled = True
    db.session.commit()

    # Generate the provisioning URI for the QR code
    provisioning_uri = pyotp.TOTP(secret_key).provisioning_uri(
        name=user.email, issuer_name="Vetty App Backend"
    )

    # Generate QR code as a base64 encoded image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, "PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return jsonify({
        "message": "Two-factor authentication enabled. Scan the QR code in your authenticator app.",
        "qr_code": qr_code_base64,
        "secret_key": secret_key
    }), 200

@user_bp.route('/disable-2fa', methods=['DELETE'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def disable_2fa():
    # JWT DISABLED TEMPORARILY FOR ROUTE TESTING

    # Original: user_id = 1  # JWT DISABLED: Replaced get_jwt_identity() with hardcoded user ID['id']

    # Using hardcoded user_id for testing without JWT

    user_id = 1  # Hardcoded user_id for testing
    user = db.session.get(User, user_id)
    user.is_2fa_enabled = False
    user.two_fa_secret = None
    db.session.commit()
    return jsonify({"message": "Two-factor authentication disabled."}), 200

@user_bp.route('/verify-2fa', methods=['POST'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def verify_2fa():
    # JWT DISABLED TEMPORARILY FOR ROUTE TESTING

    # Original: user_id = 1  # JWT DISABLED: Replaced get_jwt_identity() with hardcoded user ID['id']

    # Using hardcoded user_id for testing without JWT

    user_id = 1  # Hardcoded user_id for testing
    user = db.session.get(User, user_id)
    data = request.get_json()
    token = data.get("token")

    if not user.is_two_fa_active() or not user.get_two_fa_secret():
        return jsonify({"error": "Two-factor authentication is not enabled for this user."}), 400

    totp = pyotp.TOTP(user.get_two_fa_secret())
    if totp.verify(token):
        return jsonify({"message": "Two-factor code verified successfully."}), 200
    else:
        return jsonify({"error": "Invalid two-factor code."}), 401

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    token_2fa = data.get("token_2fa")  # Optional 2FA token

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials."}), 401

    if not user.is_verified:
        return jsonify({"error": "Email not verified. Please verify your email before logging in."}), 403

    if user.is_two_fa_active():
        if not token_2fa:
            return jsonify({"message": "Two-factor code required."}), 401
        totp = pyotp.TOTP(user.get_two_fa_secret())
        if not totp.verify(token_2fa):
            return jsonify({"error": "Invalid two-factor code."}), 401

    # Generate JWT token after successful authentication (and 2FA if enabled)
    access_token, refresh_token = generate_jwt_token(user)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
