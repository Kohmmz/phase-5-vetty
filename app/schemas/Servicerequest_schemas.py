from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validates, ValidationError
from app.models.Service_request import ServiceRequest
from app import db
from sqlalchemy.sql import func

class ServiceRequestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceRequest
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    user_id = auto_field(required=True)
    service_id = auto_field(required=True)
    status = auto_field(required=True)
    appointment_time = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    @validates("status")
    def validate_status(self, value):
        allowed = ["pending", "confirmed", "completed", "cancelled"]
        if value not in allowed:
            raise ValidationError(f"Status must be one of: {', '.join(allowed)}.")

    @validates("appointment_time")
    def validate_appointment_time(self, value):
        if value < func.now() :
            raise ValidationError("Appointment time must be in the future.")