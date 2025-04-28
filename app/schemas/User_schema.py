from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    
    id = fields.Int(dump_only=True)  
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)  # Username must be between 3 and 50 characters
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=100) # Email must be a valid email address less than 100 characters
    )
    password = fields.Str(
        required=True,
        load_only=True,  # Password should not be serialized (only deserialized)
        validate=validate.Length(min=6)  # Password must be at least 6 characters
    )
    created_at = fields.DateTime(dump_only=True)  
    updated_at = fields.DateTime(dump_only=True)  


user_schema = UserSchema() 
users_schema = UserSchema(many=True) 