from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object("app.config.Config")

    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Configure CORS
    frontend_urls = app.config.get('FRONTEND_URLS', [])
    local_urls = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://localhost:5174',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173',
        'http://127.0.0.1:5174'
    ]
    all_allowed_origins = frontend_urls + local_urls
    CORS(app, origins=all_allowed_origins, supports_credentials=True)
    print(f"CORS enabled for: {all_allowed_origins}")

    # Import and register blueprints
    from app.routes import (
        user_bp,
        auth_bp,
        admin_bp,
        cart_bp,
        cart_item_bp,
        product_bp,
        # payment_bp,
        order_bp,
        service_bp,
        service_request_bp,
    )
    from app.api_docs import api_docs_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(cart_item_bp)
    app.register_blueprint(product_bp)
    # app.register_blueprint(payment_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(service_request_bp)
    app.register_blueprint(api_docs_bp)

    return app
