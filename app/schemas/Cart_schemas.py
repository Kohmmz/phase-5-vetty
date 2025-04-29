from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.Cart import Cart

class CartSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True