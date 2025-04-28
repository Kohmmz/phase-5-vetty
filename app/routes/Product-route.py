from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app import db
from app.models.product import Product
from app.schemas.product_schema import ProductSchema  # Your schema file

product_bp = Blueprint('product_bp', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# GET /products - list all products
@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products), 200

# GET /products/<id> - get single product
@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product), 200

# POST /products - create new product
@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        validated_data = product_schema.load(data)
        new_product = Product(**validated_data)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created', 'id': new_product.id}), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

# PUT/PATCH /products/<id> - update product
@product_bp.route('/products/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    try:
        validated_data = product_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(product, key, value)
        db.session.commit()
        return jsonify({'message': 'Product updated'}), 200
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

# DELETE /products/<id> - delete product
@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200
