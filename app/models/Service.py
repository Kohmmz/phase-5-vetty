from datetime import datetime
from app import db

class Service(db.Model):
    __tablename__ = 'services'

#    Defining the columns for the services table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)
    order_items = db.relationship('OrderItem', backref='service', lazy=True)

    def __repr__(self):
        return f"<Service id={self.id} name={self.name} price={self.price}>"
