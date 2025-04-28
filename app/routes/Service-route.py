from flask import Blueprint, request, jsonify
from app import db
from app.models.Service import Service
from app.schemas.Service-schemas import ServiceSchema


# from app.models.ServiceRequest import ServiceRequest
service_bp = Blueprint('service', __name__, url_prefix='/services')
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

# Geting all services
@service_bp.route('/', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify(services_schema.dump(services)), 200

# Get services by ID
@service_bp.route('/<int:id>', methods=['GET'])
def get_service(id):
    service = Service.query.get_or_404(id)
    return jsonify(service_schema.dump(service)), 200

# Create service
@service_bp.route('/', methods=['POST'])
def create_service():
    data = request.get_json()
    errors = service_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_service = Service(
        name=data['name'],
        description=data.get('description'),
        price=data['price']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify(service_schema.dump(new_service)), 201
  # Update service
@service_bp.route('/<int:id>', methods=['PUT'])
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    errors = service_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    service.name = data['name']
    service.description = data.get('description')
    service.price = data['price']
    db.session.commit()
    return jsonify(service_schema.dump(service)), 200

# Deleting service
@service_bp.route('/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return '', 204
