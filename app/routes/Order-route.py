from flask import Blueprint, request, jsonify
from app import db
from models import Order
from marshmallow import Schema, fields, ValidationError, validate
from datetime import datetime


order_bp = Blueprint('order_bp', __name__)

# Order Schema for validation and serialization
class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    status = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    timestamp = fields.DateTime(dump_only=True)
    total_price = fields.Float(required=True, validate=validate.Range(min=0.0))


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# GET /orders - List all orders
@order_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders), 200

# GET /orders/<id> - Retrieve a single order
@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return order_schema.jsonify(order), 200

# POST /orders - Create a new order
@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        validated_data = order_schema.load(data)
        new_order = Order(
            user_id=validated_data['user_id'],
            status=validated_data['status'],
            total_price=validated_data['total_price']
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created', 'id': new_order.id}), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

# PUT/PATCH /orders/<id> - Update an order
@order_bp.route('/orders/<int:order_id>', methods=['PUT', 'PATCH'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    try:
        validated_data = order_schema.load(data, partial=True)
        if 'user_id' in validated_data:
            order.user_id = validated_data['user_id']
        if 'status' in validated_data:
            order.status = validated_data['status']
        if 'total_price' in validated_data:
            order.total_price = validated_data['total_price']
        db.session.commit()
        return jsonify({'message': 'Order updated'}), 200
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

# DELETE /orders/<id> - Delete an order
@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'}), 200
