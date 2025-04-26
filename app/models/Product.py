from flask import Flask
from app import db
from flask_sqlalchemy import SQLALchemy

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    stock = db.Column(db.Integer, nullable=False)