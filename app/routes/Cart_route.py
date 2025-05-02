from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app import db
from app.models.Cart import Cart
from app.schemas.Cart_schemas import CartSchema

cart_bp = Blueprint('cart', __name__, url_prefix='/carts')

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

@cart_bp.route('/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    cart = Cart.query.get_or_404(cart_id)
    return jsonify(cart_schema.dump(cart)), 200

@cart_bp.route('/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    cart = Cart.query.get_or_404(cart_id)
    db.session.delete(cart)
    db.session.commit()
    return "", 204

@cart_bp.route('', methods=['GET'])
def get_carts():
    carts = Cart.query.all()
    return jsonify(carts_schema.dump(carts)), 200

@cart_bp.route('', methods=['POST'])
def create_cart():
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
        return jsonify(cart_schema.dump(cart)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except KeyError as err:
        return jsonify({"errors": f"Missing required field: {err}"}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error creating cart: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500