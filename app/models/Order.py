from datetime import datetime
from app import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Assume User model exists

    # Define the many-to-many relationship with Product through ProductOrderModel
    products = db.relationship('ProductOrder', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'
