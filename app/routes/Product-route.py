from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Product

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.name for product in products])

@products_bp.route('/product', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        price=data['price'],
        description=data.get('description', ''),
        stock=data['stock']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"msg": "Product added"}), 201
