from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from marshmallow import ValidationError
from app import db
from app.models.User import User
from app.schemas.User_schema import UserSchema
from app.utils.jwt_utils import generate_jwt_token
from app.utils.email_util import send_verification_email
import random

user_bp = Blueprint('user', __name__, url_prefix='/users')
api = Api(user_bp)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Temporary store for OTPs (use a database or cache in production)
otp_store = {}

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user), 200

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        try:
            user_schema.load(data, instance=user, partial=False)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        db.session.commit()
        return user_schema.dump(user), 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users), 200

    def post(self):
        data = request.get_json()
        try:
            user = user_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        db.session.add(user)
        db.session.commit()

        # Generate OTP and send verification email
        otp = random.randint(100000, 999999)
        otp_store[user.email] = otp
        send_verification_email(user.email, otp)

        return {"message": "User created. Verification email sent."}, 201

class VerifyOTPResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        otp = data.get("otp")

        if email in otp_store and otp_store[email] == otp:
            del otp_store[email]
            return {"message": "Email verified successfully."}, 200
        return {"error": "Invalid OTP or email."}, 400

api.add_resource(UserListResource, '')
api.add_resource(UserResource, '/<int:user_id>')
api.add_resource(VerifyOTPResource, '/verify-otp')