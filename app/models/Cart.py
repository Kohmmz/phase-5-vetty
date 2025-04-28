from flask import Flask
from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#relationships
    user = db.relationship('User', back_populates='cart')
    products = db.relationship('Product', secondary='cart_items', back_populates='carts')
    services = db.relationship('Service', secondary='cart_items', back_populates='carts')