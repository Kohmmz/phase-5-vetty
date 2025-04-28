from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, validates
from marshmallow import ValidationError, validate, fields 
from app.models.Productorder import ProductOrder  
from app import db

class ProductOrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductOrder  # Link the schema to the ProductOrder model
        sqla_session = db.session  # Use the SQLAlchemy session
        load_instance = True  # Deserialize to a ProductOrder model instance
        include_fk = True  # Include foreign keys in the schema
        ordered = True  # Ensure serialized output is ordered

    # Fields with validation
    id = auto_field(dump_only=True)

    order_id = auto_field(
        required=True,
        error_messages={
            "required": "Order ID is required."
        }
    )

    product_id = auto_field(
        required=True,
        error_messages={
            "required": "Product ID is required."
        }
    )

    quantity = auto_field(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Quantity is required.",
            "range": "Quantity must be at least 1."
        }
    )

    # Relationships
    order = fields.Nested('OrderSchema', only=['id', 'status'], dump_only=True)  # Serialize related order
    product = fields.Nested('ProductSchema', only=['id', 'name', 'price'], dump_only=True)  # Serialize related product

    # Custom validation for quantity
    @validates('quantity')
    def validate_quantity(self, quantity):
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")