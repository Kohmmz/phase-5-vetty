from flask import Blueprint, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from app import db
from app.models.CartItem import CartItem
from app.schemas.CartItem_schema import CartItemSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_item_bp = Blueprint('cart_item', __name__, url_prefix='/carts/items')
api = Api(cart_item_bp)

cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

class CartItemResource(Resource):
    @jwt_required()
    def get(self, item_id):
        """Get a cart item by ID"""
        try:
            cart_item = CartItem.query.get_or_404(item_id)
            return cart_item_schema.dump(cart_item), 200
        except Exception as e:
            print(f"Error getting cart item {item_id}: {str(e)}")
            return {"error": "Error retrieving cart item"}, 500

    @jwt_required()
    def put(self, item_id):
        """Update a cart item"""
        try:
            cart_item = CartItem.query.get_or_404(item_id)
            data = request.get_json()
            
            if 'quantity' in data:
                cart_item.quantity = data['quantity']
            
            db.session.commit()
            return cart_item_schema.dump(cart_item), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error updating cart item {item_id}: {str(e)}")
            return {"error": "Error updating cart item"}, 500

    @jwt_required()
    def delete(self, item_id):
        """Delete a cart item"""
        try:
            cart_item = CartItem.query.get_or_404(item_id)
            db.session.delete(cart_item)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting cart item {item_id}: {str(e)}")
            return {"error": "Error deleting cart item"}, 500

class CartItemListResource(Resource):
    @jwt_required()
    def post(self):
        """Add an item to a cart"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'cart_id' not in data:
                return {"error": "cart_id is required"}, 400
            if 'quantity' not in data:
                return {"error": "quantity is required"}, 400
            if 'product_id' not in data and 'service_id' not in data:
                return {"error": "Either product_id or service_id is required"}, 400
            
            # Create cart item
            from datetime import datetime
            now = datetime.now()
            
            cart_item = CartItem(
                cart_id=data['cart_id'],
                product_id=data.get('product_id'),
                service_id=data.get('service_id'),
                quantity=data['quantity'],
                created_at=now
            )
            
            db.session.add(cart_item)
            db.session.commit()
            
            return cart_item_schema.dump(cart_item), 201
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error adding item to cart: {str(e)}")
            return {"error": "Error adding item to cart"}, 500

# Register resources
api.add_resource(CartItemListResource, '')
api.add_resource(CartItemResource, '/<int:item_id>')
