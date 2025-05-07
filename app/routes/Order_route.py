from flask import Blueprint, request, jsonify
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
from marshmallow import ValidationError
from app import db
from app.models.Order import Order
from app.models.OrderItem import OrderItem
from app.schemas.Order_schemas import OrderSchema
from app.schemas.Orderitem_schemas import OrderItemSchema
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order', __name__, url_prefix='/orders')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)

@order_bp.route('/<int:order_id>', methods=['GET'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def get_order(order_id):
    """
    Get a specific order by ID.
    """
    order = Order.query.get_or_404(order_id)
    return jsonify(order_schema.dump(order)), 200

@order_bp.route('/<int:order_id>', methods=['PUT'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def update_order(order_id):
    """
    Update an existing order.
    """
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    try:
        order_schema.load(data, instance=order, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    db.session.commit()
    return jsonify(order_schema.dump(order)), 200

@order_bp.route('/<int:order_id>', methods=['DELETE'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def delete_order(order_id):
    """
    Delete an order by ID.
    """
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return "", 204

@order_bp.route('', methods=['GET'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def get_orders():
    """
    Get all orders for the authenticated user.
    """
    # JWT DISABLED TEMPORARILY FOR ROUTE TESTING

    # Original: current_user = 1  # JWT DISABLED: Replaced get_jwt_identity() with hardcoded user ID

    # Using hardcoded user identity for testing without JWT

    current_user = {"id": 1, "role": "User"}
    orders = Order.query.filter_by(user_id=current_user["id"]).all()
    return jsonify(orders_schema.dump(orders)), 200

@order_bp.route('', methods=['POST'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def create_order():
    """
    Create a new order.
    """
    data = request.get_json()
    # JWT DISABLED TEMPORARILY FOR ROUTE TESTING

    # Original: current_user = 1  # JWT DISABLED: Replaced get_jwt_identity() with hardcoded user ID

    # Using hardcoded user identity for testing without JWT

    current_user = {"id": 1, "role": "User"}

    # Validate and create the order
    try:
        order_data = {
            "user_id": current_user["id"],
            "total_price": data.get("total_price"),
            "status": "pending"
        }
        order = order_schema.load(order_data)
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID for order items

        # Add order items
        for item in data.get("items", []):
            item["order_id"] = order.id
            order_item = order_item_schema.load(item)
            db.session.add(order_item)

        db.session.commit()
        return jsonify(order_schema.dump(order)), 201
    except ValidationError as err:
        db.session.rollback()
        return jsonify({"errors": err.messages}), 400

@order_bp.route('/<int:order_id>/items', methods=['GET'])
# JWT DISABLED TEMPORARILY FOR ROUTE TESTING
# @jwt_required()
def get_order_items(order_id):
    """
    Get all items for a specific order.
    """
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    return jsonify(order_items_schema.dump(order_items)), 200