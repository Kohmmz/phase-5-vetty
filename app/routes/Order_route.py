from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from marshmallow import ValidationError
from app import db
from app.models.Order import Order
from app.models.OrderItem import OrderItem
from app.schemas.Order_schemas import OrderSchema
from app.schemas.Orderitem_schemas import OrderItemSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order', __name__, url_prefix='/orders')
api = Api(order_bp)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)

class OrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        """
        Get a specific order by ID.
        """
        order = Order.query.get_or_404(order_id)
        return order_schema.dump(order), 200

    @jwt_required()
    def put(self, order_id):
        """
        Update an existing order.
        """
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        try:
            order_schema.load(data, instance=order, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        db.session.commit()
        return order_schema.dump(order), 200

    @jwt_required()
    def delete(self, order_id):
        """
        Delete an order by ID.
        """
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return {}, 204

class OrderListResource(Resource):
    @jwt_required()
    def get(self):
        """
        Get all orders for the authenticated user.
        """
        current_user = get_jwt_identity()
        orders = Order.query.filter_by(user_id=current_user["id"]).all()
        return orders_schema.dump(orders), 200

    @jwt_required()
    def post(self):
        """
        Create a new order.
        """
        data = request.get_json()
        current_user = get_jwt_identity()

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
            return order_schema.dump(order), 201
        except ValidationError as err:
            db.session.rollback()
            return {"errors": err.messages}, 400

class OrderItemResource(Resource):
    @jwt_required()
    def get(self, order_id):
        """
        Get all items for a specific order.
        """
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        return order_items_schema.dump(order_items), 200

api.add_resource(OrderListResource, '')
api.add_resource(OrderResource, '/<int:order_id>')
api.add_resource(OrderItemResource, '/<int:order_id>/items')