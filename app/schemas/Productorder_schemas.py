from marshmallow import Schema, fields, validate

class ProductOrderSchema(Schema):
    
    id = fields.Int(dump_only=True)  
    order_id = fields.Int(required=True)  
    product_id = fields.Int(required=True)  
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1)  # Quantity must be at least 1
    )

    
    order = fields.Nested('OrderSchema', only=['id', 'status'], dump_only=True)  
    product = fields.Nested('ProductSchema', only=['id', 'name', 'price'], dump_only=True)  

# Create schema instances for single and multiple ProductOrder objects
product_order_schema = ProductOrderSchema()  
product_orders_schema = ProductOrderSchema(many=True)  