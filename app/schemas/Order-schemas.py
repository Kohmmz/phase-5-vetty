from marshmallow import Schema, fields

class OrderSchema(Schema):
    # Order schema for serializing and deserializing order data
    id = fields.Int(dump_only=True)
    # Foreign key to the  tables
    user_id = fields.Int(required=True)
    status = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    order_items = fields.Nested('OrderItemSchema', many=True, dump_only=True)
