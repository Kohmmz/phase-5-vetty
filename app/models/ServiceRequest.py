from datetime import datetime
from app import db

class ServiceBooking(db.Model):
    __tablename__ = 'service_bookings'

    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to the  tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#    # Relationships
    def __repr__(self):
        return f"<ServiceBooking id={self.id} user_id={self.user_id} service_id={self.service_id} appointment_time={self.appointment_time}>"
