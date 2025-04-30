from flask import Blueprint, request, jsonify
from app.models.User import User
from app.models.Order import Order
from app.models.Product import Product
from app import db
from app.utils.auth_util import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@role_required("Admin")
def get_all_users():
    """
    Get all users in the system (Admin only).
    """
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    } for user in users]), 200

@admin_bp.route('/admin/orders', methods=['GET'])
@role_required("Admin")
def get_all_orders():
    """
    Get all orders in the system (Admin only).
    """
    orders = Order.query.all()
    return jsonify([{
        "id": order.id,
        "user_id": order.user_id,
        "total_price": order.total_price,
        "status": order.status,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    } for order in orders]), 200

@admin_bp.route('/admin/products/<int:product_id>/stock', methods=['PUT'])
@role_required("Admin")
def update_stock(product_id):
    """
    Update the stock quantity of a product (Admin only).
    """
    data = request.get_json()
    product = Product.query.get_or_404(product_id)
    if "stock_quantity" not in data:
        return jsonify({"error": "stock_quantity is required"}), 400

    product.stock_quantity = data["stock_quantity"]
    db.session.commit()
    return jsonify({"message": "Stock updated successfully", "product_id": product.id, "stock_quantity": product.stock_quantity}), 200

@admin_bp.route('/admin/stats/revenue', methods=['GET'])
@role_required("Admin")
def get_revenue_stats():
    """
    Get revenue statistics (Admin only).
    """
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    total_orders = Order.query.count()
    return jsonify({
        "total_revenue": total_revenue,
        "total_orders": total_orders
    }), 200