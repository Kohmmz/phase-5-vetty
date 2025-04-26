from flask import Blueprint, request, jsonify
from app import db
from app.models.Order import Order
from app.models.OrderItem import OrderItem
from app.models.Product import Product
from app.schemas.Order-schemas import OrderSchema
from app.schemas.Orderitem-schemas import OrderItemSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
# from datetime import datetime
order_bp = Blueprint('order_bp', __name__, url_prefix='/orders')

@order_bp.route('/', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    # ton Validate stock availability
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'No items provided'}), 400

    for item in items:
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({'error': f"Product id {item['product_id']} not found"}), 404
        if product.stock < item['quantity']:
            return jsonify({'error': f"Insufficient stock for product id {item['product_id']}"}), 400

    # Creating order
    order = Order(user_id=user_id, status='pending')
    db.session.add(order)
    db.session.flush()  # to get order with.id

    # Creating order items and reduce stock
    for item in items:
        order_item = OrderItem(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'])
        db.session.add(order_item)
        product = Product.query.get(item['product_id'])
        product.stock -= item['quantity']

    db.session.commit()

    order_schema = OrderSchema()
    return order_schema.jsonify(order), 201

@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    order_schema = OrderSchema(many=True)
    return order_schema.jsonify(orders), 200
