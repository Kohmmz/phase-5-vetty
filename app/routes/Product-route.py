from flask import Blueprint, request, jsonify, abort
from app import db
from models import Product
from app.schemas.Product_schemas import product_schema, products_schema
from marshmallow.exceptions import ValidationError

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    if not products:
        return jsonify({'message': 'No products found'}), 404
    return jsonify(products_schema.dump(products)), 200  # Serialize and return as JSON

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product_schema.dump(product)), 200  # Serialize and return as JSON

@product_bp.route('/products', methods=['POST'])
def create_product():
    try:
        # Deserialize and validate incoming JSON data
        product_data = product_schema.load(request.json)
        # Create a new Product instance
        new_product = Product(**product_data)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created', 'id': new_product.id}), 201  # Return the created product
    except ValidationError as e:
        # Handle validation errors
        return jsonify({'error': e.messages}), 400
    except Exception as e:
        # Handle other errors
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        # Deserialize and validate incoming JSON data
        product_data = product_schema.load(request.json)
        # Update product attributes dynamically
        for key, value in product_data.items():
            setattr(product, key, value)
        db.session.commit()
        return jsonify({'message': 'Product updated'}), 200  # Return a success message
    except ValidationError as e:
        # Handle validation errors
        return jsonify({'error': e.messages}), 400
    except Exception as e:
        # Handle other errors
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200