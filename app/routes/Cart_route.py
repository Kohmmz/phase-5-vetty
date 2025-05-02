from flask import Blueprint, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from app import db
from app.models.Cart import Cart
from app.schemas.Cart_schemas import CartSchema

cart_bp = Blueprint('cart', __name__, url_prefix='/carts')
api = Api(cart_bp)

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

class CartResource(Resource):
    def get(self, cart_id):
        cart = Cart.query.get_or_404(cart_id)
        return cart_schema.dump(cart), 200

    def delete(self, cart_id):
        cart = Cart.query.get_or_404(cart_id)
        db.session.delete(cart)
        db.session.commit()
        return {}, 204

class CartListResource(Resource):
    def get(self):
        carts = Cart.query.all()
        return carts_schema.dump(carts), 200

    def post(self):
        data = request.get_json()
        try:
            from datetime import datetime
            now = datetime.now()
            
            cart = Cart(
                user_id=data['user_id'],
                updated_at=now
            )
            
            db.session.add(cart)
            db.session.commit()
            return cart_schema.dump(cart), 201
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except KeyError as err:
            return {"errors": f"Missing required field: {err}"}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error creating cart: {str(e)}")
            return {"message": "Internal Server Error"}, 500

api.add_resource(CartListResource, '')
api.add_resource(CartResource, '/<int:cart_id>')