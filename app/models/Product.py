from flask import Flask
from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Line-item relationships
    cart_items = db.relationship('CartItem', back_populates='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', back_populates='product', lazy=True, cascade='all, delete-orphan')

    