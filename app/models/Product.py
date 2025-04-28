from app import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Define the many-to-many relationship with Order through ProductOrderModel
    orders = db.relationship('ProductOrder', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'