from flask import Blueprint, jsonify

# Create a Blueprint for the API documentation
api_docs_bp = Blueprint('api_docs', __name__, url_prefix='/api/docs')

@api_docs_bp.route('/')
def api_docs():
    """Return API documentation in JSON format"""
    api_documentation = {
        "version": "1.0",
        "title": "Vetty Backend API",
        "description": "API documentation for the Vetty Backend application",
        "endpoints": {
            "auth": {
                "signup": {
                    "url": "/signup",
                    "method": "POST",
                    "description": "Create a new user account",
                    "request_body": {
                        "username": "string",
                        "email": "string",
                        "password": "string"
                    },
                    "responses": {
                        "201": "User created successfully",
                        "400": "Validation error"
                    }
                },
                "login": {
                    "url": "/login",
                    "method": "POST",
                    "description": "Login with existing credentials",
                    "request_body": {
                        "email": "string",
                        "password": "string"
                    },
                    "responses": {
                        "200": "Login successful",
                        "401": "Invalid credentials"
                    }
                },
                "logout": {
                    "url": "/logout",
                    "method": "POST",
                    "description": "Logout the current user",
                    "responses": {
                        "200": "Logout successful"
                    }
                }
            },
            "users": {
                "get_all_users": {
                    "url": "/users",
                    "method": "GET",
                    "description": "Get all users",
                    "responses": {
                        "200": "Success"
                    }
                },
                "get_user": {
                    "url": "/users/{user_id}",
                    "method": "GET",
                    "description": "Get a specific user by ID",
                    "responses": {
                        "200": "Success",
                        "404": "User not found"
                    }
                }
            },
            "products": {
                "get_all_products": {
                    "url": "/products",
                    "method": "GET",
                    "description": "Get all products",
                    "responses": {
                        "200": "Success"
                    }
                },
                "create_product": {
                    "url": "/products",
                    "method": "POST",
                    "description": "Create a new product",
                    "request_body": {
                        "name": "string",
                        "description": "string",
                        "price": "number"
                    },
                    "responses": {
                        "201": "Product created",
                        "400": "Validation error"
                    }
                },
                "get_product": {
                    "url": "/products/{product_id}",
                    "method": "GET",
                    "description": "Get a specific product by ID",
                    "responses": {
                        "200": "Success",
                        "404": "Product not found"
                    }
                }
            },
            "services": {
                "get_all_services": {
                    "url": "/services",
                    "method": "GET",
                    "description": "Get all services",
                    "responses": {
                        "200": "Success"
                    }
                },
                "create_service": {
                    "url": "/services",
                    "method": "POST",
                    "description": "Create a new service",
                    "request_body": {
                        "name": "string",
                        "description": "string",
                        "price": "number"
                    },
                    "responses": {
                        "201": "Service created",
                        "400": "Validation error"
                    }
                },
                "get_service": {
                    "url": "/services/{service_id}",
                    "method": "GET",
                    "description": "Get a specific service by ID",
                    "responses": {
                        "200": "Success",
                        "404": "Service not found"
                    }
                }
            },
            "carts": {
                "get_all_carts": {
                    "url": "/carts",
                    "method": "GET",
                    "description": "Get all carts",
                    "responses": {
                        "200": "Success"
                    }
                },
                "create_cart": {
                    "url": "/carts",
                    "method": "POST",
                    "description": "Create a new cart",
                    "request_body": {
                        "user_id": "integer"
                    },
                    "responses": {
                        "201": "Cart created",
                        "400": "Validation error"
                    }
                },
                "get_cart": {
                    "url": "/carts/{cart_id}",
                    "method": "GET",
                    "description": "Get a specific cart by ID",
                    "responses": {
                        "200": "Success",
                        "404": "Cart not found"
                    }
                },
                "delete_cart": {
                    "url": "/carts/{cart_id}",
                    "method": "DELETE",
                    "description": "Delete a cart by ID",
                    "responses": {
                        "204": "Cart deleted",
                        "404": "Cart not found"
                    }
                },
                "add_cart_item": {
                    "url": "/carts/items",
                    "method": "POST",
                    "description": "Add an item to a cart",
                    "request_body": {
                        "cart_id": "integer",
                        "product_id": "integer (optional)",
                        "service_id": "integer (optional)",
                        "quantity": "integer"
                    },
                    "responses": {
                        "201": "Cart item created",
                        "400": "Validation error"
                    }
                }
            },
            "orders": {
                "get_all_orders": {
                    "url": "/orders",
                    "method": "GET",
                    "description": "Get all orders for the authenticated user",
                    "responses": {
                        "200": "Success"
                    }
                },
                "create_order": {
                    "url": "/orders",
                    "method": "POST",
                    "description": "Create a new order",
                    "request_body": {
                        "total_price": "number",
                        "items": [
                            {
                                "product_id": "integer (optional)",
                                "service_id": "integer (optional)",
                                "quantity": "integer",
                                "unit_price": "number"
                            }
                        ]
                    },
                    "responses": {
                        "201": "Order created",
                        "400": "Validation error"
                    }
                },
                "get_order": {
                    "url": "/orders/{order_id}",
                    "method": "GET",
                    "description": "Get a specific order by ID",
                    "responses": {
                        "200": "Success",
                        "404": "Order not found"
                    }
                },
                "get_order_items": {
                    "url": "/orders/{order_id}/items",
                    "method": "GET",
                    "description": "Get all items for a specific order",
                    "responses": {
                        "200": "Success",
                        "404": "Order not found"
                    }
                }
            }
        }
    }
    return jsonify(api_documentation)
