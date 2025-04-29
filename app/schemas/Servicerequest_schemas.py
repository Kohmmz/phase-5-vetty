from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from app.models.Service_request import ServiceRequest

class ServiceRequestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceRequest
        load_instance = True

    @validates("appointment_time")
    def validate_appointment_time(self, value):
        if value is None:
            raise ValidationError("Appointment time is required.")