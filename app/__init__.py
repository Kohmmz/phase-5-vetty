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

    # Enable CORS with support for any localhost URL
    if app.config.get('DEBUG', False):
        # In development mode, allow any origin
        CORS(app, supports_credentials=True)
    else:
        # In production, only allow the production URL
        production_url = app.config.get('FRONTEND_URL', 'https://vetty-frontend.netlify.app').split(',')[0].strip()
        CORS(app, origins=[production_url], supports_credentials=True)

    # Import and register all blueprints
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
    # Import API documentation blueprint
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
    app.register_blueprint(api_docs_bp)  # Register API docs blueprint

    return app
