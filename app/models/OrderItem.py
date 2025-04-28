from app import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'
#    # Define the columns for the order items table
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to the orders table
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)

#    # Relationships
    def __repr__(self):
        return f"<OrderItem id={self.id} order_id={self.order_id} product_id={self.product_id} service_id={self.service_id} quantity={self.quantity}>"