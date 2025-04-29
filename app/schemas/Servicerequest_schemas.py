from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, validates
from marshmallow import ValidationError, validate
from app.models.servicerequest import ServiceRequest  # Adjust the import path as needed
from app import db

class ServiceRequestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceRequest
        sqla_session = db.session
        load_instance = True
        include_fk = True
        ordered = True

    id = auto_field(dump_only=True)

    user_id = auto_field(required=True, error_messages={"required": "User ID is required."})
    service_id = auto_field(required=True, error_messages={"required": "Service ID is required."})

    status = auto_field(
        required=True,
        validate=validate.OneOf(["pending", "approved", "completed", "cancelled"]),
        error_messages={
            "required": "Status is required.",
            "validator_failed": "Status must be one of: pending, approved, completed, cancelled."
        }
    )

    notes = auto_field(
        required=False,
        validate=validate.Length(max=500),
        error_messages={"length": "Notes cannot exceed 500 characters."}
    )

    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    @validates('notes')
    def validate_notes_length(self, notes):
        if notes and len(notes.strip()) < 3:
            raise ValidationError("Notes must be at least 3 characters long if provided.")
