from app import db

class ProductOrder(db.Model):
    __tablename__ = 'product_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relationships
    order = db.relationship('Order', backref=db.backref('product_orders', lazy=True))
    product = db.relationship('Product', backref=db.backref('product_orders', lazy=True))

    def __repr__(self):
        return f"<ProductOrder Order ID: {self.order_id} Product ID: {self.product_id} Quantity: {self.quantity}>"
