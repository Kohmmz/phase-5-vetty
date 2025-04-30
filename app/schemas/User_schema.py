from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, validates
from marshmallow import ValidationError, fields
from app.models.User import User  
from app import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)  

    password = fields.String(required=True, load_only=True)
    confirm_password = fields.String(required=True, load_only=True)

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter.")

    @validates("email")
    def validate_email(self, value):
        if "@" not in value or "." not in value:
            raise ValidationError("Invalid email address.")