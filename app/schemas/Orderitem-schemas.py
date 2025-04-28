from marshmallow import Schema, fields
# Service schema for serializing and deserializing service data
class OrderItemSchema(Schema):
    
    # Defining fields for the order item schema
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    product_id = fields.Int(allow_none=True)
    service_id = fields.Int(allow_none=True)
    quantity = fields.Int(required=True)
