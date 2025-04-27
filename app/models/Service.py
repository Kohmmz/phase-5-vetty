from flask import Flask
from app import db#Not set up yet
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default =datetime.utcnow, onupdate=datetime.utcnow)
    
    #relationships
    order = db.relationship('Order', back_populates ='service', cascade='all, delete-orphan')
    serviceRequest = db.relationship('ServiceRequest', back_populates ='service', cascade='all, delete-orphan')
