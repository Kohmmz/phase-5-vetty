from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, validates
from marshmallow import ValidationError, validate
from app.models.Order import Order
from app import db
from app.schemas.Orderitem_schemas import OrderItemSchema  # Adjust import if needed


class OrderSchema(SQLAlchemyAutoSchema):
#    """Schema for serializing and deserializing Order objects."""
    class Meta:
        model = Order
        sqla_session = db.session
        load_instance = True
        include_fk = True
        ordered = True
#        # Include the OrderItemSchema for nested serialization
    id = auto_field(dump_only=True)
    user_id = auto_field(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "User ID is required.",
            "range": "User ID must be a positive integer."
        }
    )
    status = auto_field(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={
            "required": "Status is required.",
            "length": "Status must be between 1 and 50 characters."
        }
    )
    timestamp = auto_field(dump_only=True)
    total_price = auto_field(dump_only=True)
    order_items = auto_field(dump_only=True)

    @validates('status')
    def validate_status(self, value):
        if len(value) < 3:
            raise ValidationError("Status must be at least 3 characters long.")
