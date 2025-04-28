from flask import Blueprint, request, jsonify, abort
from app import db
from models import Service
from app.schemas.Service_schemas import service_schema, services_schema
from marshmallow.exceptions import ValidationError

service_bp = Blueprint('service_bp', __name__)

@service_bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify(services_schema.dump(services)), 200  # Serialize and return as JSON

@service_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify(service_schema.dump(service)), 200  # Serialize and return as JSON

@service_bp.route('/services', methods=['POST'])
def create_service():
    try:
        # Deserialize and validate incoming JSON data
        service_data = service_schema.load(request.json)
        # Create a new Service instance
        new_service = Service(**service_data)
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message': 'Service created', 'id': new_service.id}), 201  # Return the created service
    except ValidationError as e:
        # Handle validation errors
        return jsonify({'error': e.messages}), 400
    except Exception as e:
        # Handle other errors
        return jsonify({'error': str(e)}), 400

@service_bp.route('/services/<int:service_id>', methods=['PUT', 'PATCH'])
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    try:
        # Deserialize and validate incoming JSON data
        service_data = service_schema.load(request.json)
        # Update service attributes dynamically
        for key, value in service_data.items():
            setattr(service, key, value)
        db.session.commit()
        return jsonify({'message': 'Service updated'}), 200  # Return a success message
    except ValidationError as e:
        # Handle validation errors
        return jsonify({'error': e.messages}), 400
    except Exception as e:
        # Handle other errors
        return jsonify({'error': str(e)}), 400

# Route to delete a service
@service_bp.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted'}), 200
