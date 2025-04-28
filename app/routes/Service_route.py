from flask import Blueprint, request, jsonify, abort
from app import db
from models import Service

service_bp = Blueprint('service_bp', __name__)

@service_bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'price': s.price,
        'description': s.description,
        'created_at': s.created_at,
        'updated_at': s.updated_at
    } for s in services]), 200

@service_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify({
        'id': service.id,
        'name': service.name,
        'price': service.price,
        'description': service.description,
        'created_at': service.created_at,
        'updated_at': service.updated_at
    }), 200

@service_bp.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    try:
        new_service = Service(
            name=data['name'],
            price=data['price'],
            description=data.get('description')
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message': 'Service created', 'id': new_service.id}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

@service_bp.route('/services/<int:service_id>', methods=['PUT', 'PATCH'])
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    data = request.get_json()

    service.name = data.get('name', service.name)
    service.price = data.get('price', service.price)
    service.description = data.get('description', service.description)

    db.session.commit()
    return jsonify({'message': 'Service updated'}), 200

@service_bp.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted'}), 200