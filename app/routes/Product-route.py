from productRecources import ProductResource, ProductList

def initialize_routes(api):
    api.add_resource(ProductList, '/products')  # GET all products / POST new product
    api.add_resource(ProductResource, '/products/<int:product_id>')  # GET, DELETE, PUT for specific product
