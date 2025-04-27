from flask import Flask
from app import db#Not set up yet
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.Sring(50), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default =datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define any relationships here
    