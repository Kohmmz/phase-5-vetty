from app import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'
#    # Define the columns for the order items table
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to the orders table
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<OrderItem id={self.id} order_id={self.order_id} product_id={self.product_id} quantity={self.quantity}>"
