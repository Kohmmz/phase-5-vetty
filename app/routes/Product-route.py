from flask_restful import Resource, reqparse
from models import Product
from app import db

# Request parser for product fields
product_parser = reqparse.RequestParser()
product_parser.add_argument('name', required=True)
product_parser.add_argument('price', type=float, required=True)
product_parser.add_argument('description', required=False)
product_parser.add_argument('category', required=True)
product_parser.add_argument('stock_quantity', type=int, required=True)

class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        return [{'id': p.id, 'name': p.name, 'price': p.price} for p in products]

    def post(self):
        args = product_parser.parse_args()
        new_product = Product(**args)
        db.session.add(new_product)
        db.session.commit()
        return {'id': new_product.id, 'message': 'Product created'}, 201

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'stock_quantity': product.stock_quantity,
            'created_at': product.created_at.isoformat(),
            'updated_at': product.updated_at.isoformat(),
        }

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted'}

    def put(self, product_id):
        product = Product.query.get_or_404(product_id)
        args = product_parser.parse_args()
        for key, value in args.items():
            setattr(product, key, value)
        db.session.commit()
        return {'message': 'Product updated'}

# from productRecources import ProductResource, ProductList

# def initialize_routes(api):
#     api.add_resource(ProductList, '/products')  # GET all products / POST new product
#     api.add_resource(ProductResource, '/products/<int:product_id>')  # GET, DELETE, PUT for specific product
