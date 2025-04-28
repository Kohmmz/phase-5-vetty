from marshmallow import Schema, fields, validate

class ServiceSchema(Schema):

    id = fields.Int(dump_only=True)  
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)  # Name must be between 1 and 100 characters
    )
    price = fields.Float(
        required=True,
        validate=validate.Range(min=0)  
    )
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=500)  # Description can be up to 500 characters
    )
    created_at = fields.DateTime(dump_only=True)  
    updated_at = fields.DateTime(dump_only=True)  


service_schema = ServiceSchema()  
services_schema = ServiceSchema(many=True)  