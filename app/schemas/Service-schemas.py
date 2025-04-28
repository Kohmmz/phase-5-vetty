from marshmallow import Schema, fields
# Service schema for serializing and deserializing service data
class ServiceSchema(Schema):
    
    # DefinING  fields for the service schema
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
