from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app import db
from app.models.CartItem import CartItem
from app.schemas.CartItem_schema import CartItemSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_item_bp = Blueprint('cart_item', __name__, url_prefix='/carts/items')

cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

@cart_item_bp.route('/<int:item_id>', methods=['GET'])
@jwt_required()
def get_cart_item(item_id):
    """Get a cart item by ID"""
    try:
        cart_item = CartItem.query.get_or_404(item_id)
        return jsonify(cart_item_schema.dump(cart_item)), 200
    except Exception as e:
        print(f"Error getting cart item {item_id}: {str(e)}")
        return jsonify({"error": "Error retrieving cart item"}), 500

@cart_item_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """Update a cart item"""
    try:
        cart_item = CartItem.query.get_or_404(item_id)
        data = request.get_json()
        
        if 'quantity' in data:
            cart_item.quantity = data['quantity']
        
        db.session.commit()
        return jsonify(cart_item_schema.dump(cart_item)), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating cart item {item_id}: {str(e)}")
        return jsonify({"error": "Error updating cart item"}), 500

@cart_item_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(item_id):
    """Delete a cart item"""
    try:
        cart_item = CartItem.query.get_or_404(item_id)
        db.session.delete(cart_item)
        db.session.commit()
        return "", 204
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting cart item {item_id}: {str(e)}")
        return jsonify({"error": "Error deleting cart item"}), 500

@cart_item_bp.route('', methods=['POST'])
@jwt_required()
def add_cart_item():
    """Add an item to a cart"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'cart_id' not in data:
            return jsonify({"error": "cart_id is required"}), 400
        if 'quantity' not in data:
            return jsonify({"error": "quantity is required"}), 400
        if 'product_id' not in data and 'service_id' not in data:
            return jsonify({"error": "Either product_id or service_id is required"}), 400
        
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
        
        return jsonify(cart_item_schema.dump(cart_item)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error adding item to cart: {str(e)}")
        return jsonify({"error": "Error adding item to cart"}), 500
