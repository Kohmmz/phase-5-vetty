from marshmallow import Schema, fields

class ServiceBookingSchema(Schema):
    id = fields.Int(dump_only=True)
    # Foreign key to the  tables
    user_id = fields.Int(required=True)
    service_id = fields.Int(required=True)
    appointment_time = fields.DateTime(required=True)
    timestamp = fields.DateTime(dump_only=True)
