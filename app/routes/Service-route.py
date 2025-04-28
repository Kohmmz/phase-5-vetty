from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Service

services_bp = Blueprint('services_bp', __name__)

@services_bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.name for service in services])

@services_bp.route('/service', methods=['POST'])
@jwt_required()
def add_service():
    data = request.get_json()
    service = Service(
        name=data['name'],
        price=data['price'],
        duration=data['duration']
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({"msg": "Service added"}), 201
