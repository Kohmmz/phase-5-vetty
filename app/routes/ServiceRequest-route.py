from flask import Blueprint, request, jsonify
from app import db
from app.models.ServiceRequest import ServiceRequest
from app.schemas.Servicerequest-schemas import ServiceRequestSchema

# from app.models.Service import Service
service_request_bp = Blueprint('service_request', __name__, url_prefix='/service_requests')
service_request_schema = ServiceRequestSchema()
service_requests_schema = ServiceRequestSchema(many=True)

# Geting all service requests
@service_request_bp.route('/', methods=['GET'])
def get_service_requests():
    service_requests = ServiceRequest.query.all()
    return jsonify(service_requests_schema.dump(service_requests)), 200

# Geting service request by ID
@service_request_bp.route('/<int:id>', methods=['GET'])
def get_service_request(id):
    service_request = ServiceRequest.query.get_or_404(id)
    return jsonify(service_request_schema.dump(service_request)), 200

# Creating service request
@service_request_bp.route('/', methods=['POST'])
def create_service_request():
    data = request.get_json()
    errors = service_request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_service_request = ServiceRequest(
        user_id=data['user_id'],
        service_id=data['service_id'],
        appointment_time=data['appointment_time']
    )
    db.session.add(new_service_request)
    db.session.commit()
    return jsonify(service_request_schema.dump(new_service_request)), 201

# Updating service request
@service_request_bp.route('/<int:id>', methods=['PUT'])
def update_service_request(id):
    service_request = ServiceRequest.query.get_or_404(id)
    data = request.get_json()
    errors = service_request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    service_request.user_id = data['user_id']
    service_request.service_id = data['service_id']
    service_request.appointment_time = data['appointment_time']
    db.session.commit()
    return jsonify(service_request_schema.dump(service_request)), 200

# Deleting service request
@service_request_bp.route('/<int:id>', methods=['DELETE'])
def delete_service_request(id):
    service_request = ServiceRequest.query.get_or_404(id)
    db.session.delete(service_request)
    db.session.commit()
    return '', 204