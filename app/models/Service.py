from sqlalchemy.sql import func
from app import db

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    service_requests = db.relationship('ServiceRequest', back_populates='service', lazy=True)
    order_items = db.relationship('OrderItem', back_populates='service', lazy=True)
    cart_items = db.relationship('CartItem', back_populates='service', lazy=True)
