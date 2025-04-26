from flask import Blueprint, request, jsonify
from app import db
from app.models.ServiceBooking import ServiceBooking
from app.models.Service import Service
from app.schemas.ServiceBooking-schemas import ServiceBookingSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

service_booking_bp = Blueprint('service_booking_bp', __name__, url_prefix='/service-bookings')

@service_booking_bp.route('/', methods=['POST'])
@jwt_required()
def book_service():
    user_id = get_jwt_identity()
    data = request.get_json()

    service_id = data.get('service_id')
    appointment_time_str = data.get('appointment_time')

    if not service_id or not appointment_time_str:
        return jsonify({'error': 'service_id and appointment_time are required'}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    try:
        appointment_time = datetime.fromisoformat(appointment_time_str)
    except ValueError:
        return jsonify({'error': 'Invalid appointment_time format. Use ISO format.'}), 400

    # Checking  double booking
    existing_booking = ServiceBooking.query.filter_by(user_id=user_id, appointment_time=appointment_time).first()
    if existing_booking:
        return jsonify({'error': 'You already have a booking at this appointment time'}), 400

    # Create services booking
    booking = ServiceBooking(user_id=user_id, service_id=service_id, appointment_time=appointment_time)
    db.session.add(booking)
    db.session.commit()

    booking_schema = ServiceBookingSchema()
    return booking_schema.jsonify(booking), 201

@service_booking_bp.route('/', methods=['GET'])
@jwt_required()
def get_service_bookings():
    user_id = get_jwt_identity()
    bookings = ServiceBooking.query.filter_by(user_id=user_id).all()
    booking_schema = ServiceBookingSchema(many=True)
    return booking_schema.jsonify(bookings), 200
