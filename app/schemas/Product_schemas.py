from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, validates
from marshmallow import ValidationError, validate
from app.models.Product import Product  # Adjust import path as needed
from app import db

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        sqla_session = db.session
        load_instance = True
        include_fk = True  # Only needed if foreign keys are exposed
        ordered = True

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
        error_messages={"length": "Description cannot exceed 500 characters."}
    )

    category = auto_field(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={
            "required": "Category is required.",
            "length": "Category must be between 1 and 50 characters."
        }
    )

    stock_quantity = auto_field(
        required=True,
        validate=validate.Range(min=0),
        error_messages={
            "required": "Stock quantity is required.",
            "range": "Stock quantity must be a non-negative integer."
        }
    )

    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    # Custom validation for uniqueness
    @validates('name')
    def validate_name_unique(self, name):
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product:
            raise ValidationError("A product with this name already exists.")

    # Optional stricter check on category
    @validates('category')
    def validate_category_length(self, category):
        if len(category) < 3:
            raise ValidationError("Category must be at least 3 characters long.")