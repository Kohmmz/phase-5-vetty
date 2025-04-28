from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, validates
from marshmallow import ValidationError, validate
from app.models.Service import Service  # Adjust import path as needed
from app import db

class ServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Service  # Link the schema to the Service model
        sqla_session = db.session  # Use the SQLAlchemy session
        load_instance = True  # Deserialize to a Service model instance
        ordered = True  # Ensure serialized output is ordered

    # Fields with validation
    id = auto_field(dump_only=True)

    name = auto_field(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={
            "required": "Name is required.",
            "length": "Name must be between 1 and 100 characters."
        }
    )

    price = auto_field(
        required=True,
        validate=validate.Range(min=0),
        error_messages={
            "required": "Price is required.",
            "range": "Price must be a positive number."
        }
    )

    description = auto_field(
        required=False,
        validate=validate.Length(max=500),
        error_messages={
            "length": "Description cannot exceed 500 characters."
        }
    )

    created_at = auto_field(dump_only=True)  # Read-only field for creation timestamp
    updated_at = auto_field(dump_only=True)  # Read-only field for last update timestamp

    # Custom validation for name uniqueness
    @validates('name')
    def validate_name_unique(self, name):
        existing_service = Service.query.filter_by(name=name).first()
        if existing_service:
            raise ValidationError("A service with this name already exists.")

    # Optional stricter validation for price
    @validates('price')
    def validate_price(self, price):
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")