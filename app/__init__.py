from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.Order-route import order_bp
    from app.routes.ServiceBooking-route import service_booking_bp

    app.register_blueprint(order_bp)
    app.register_blueprint(service_booking_bp)

    return app
