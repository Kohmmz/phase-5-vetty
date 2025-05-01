from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.Product import Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'category': p.category,
        'stock_quantity': p.stock_quantity,
        'created_at': p.created_at,
        'updated_at': p.updated_at
    } for p in products]), 200

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'category': product.category,
        'stock_quantity': product.stock_quantity,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    }), 200

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            name=data['name'],
            price=data['price'],
            description=data.get('description'),
            category=data['category'],
            stock_quantity=data['stock_quantity']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created', 'id': new_product.id}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

@product_bp.route('/products/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.description = data.get('description', product.description)
    product.category = data.get('category', product.category)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)

    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200