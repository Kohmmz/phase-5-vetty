from marshmallow import Schema, fields
from datetime import datetime

# Define the schema for the Product model
class ProductSchema(Schema):
    
    id = fields.Int(dump_only=True)  
    name = fields.Str(required=True)  
    price = fields.Float(required=True)  
    description = fields.Str(allow_none=True)  
    category = fields.Str(required=True)  
    stock_quantity = fields.Int(required=True)  
    created_at = fields.DateTime(dump_only=True) 
    updated_at = fields.DateTime(dump_only=True)  

#Serialization and deserialization
product_schema = ProductSchema()  
products_schema = ProductSchema(many=True)  