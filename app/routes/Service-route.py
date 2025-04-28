from flask_restful import Resource, reqparse
from models import Service
from app import db

# Request parser for Service
service_parser = reqparse.RequestParser()
service_parser.add_argument('name', required=True)
service_parser.add_argument('price', type=float, required=True)
service_parser.add_argument('description', required=False)

class ServiceList(Resource):
    def get(self):
        services = Service.query.all()
        return [{'id': s.id, 'name': s.name, 'price': s.price} for s in services]

    def post(self):
        args = service_parser.parse_args()
        new_service = Service(**args)
        db.session.add(new_service)
        db.session.commit()
        return {'id': new_service.id, 'message': 'Service created'}, 201

class ServiceResource(Resource):
    def get(self, service_id):
        service = Service.query.get_or_404(service_id)
        return {
            'id': service.id,
            'name': service.name,
            'price': service.price,
            'description': service.description,
            'created_at': service.created_at.isoformat(),
            'updated_at': service.updated_at.isoformat(),
        }

    def delete(self, service_id):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return {'message': 'Service deleted'}

    def put(self, service_id):
        service = Service.query.get_or_404(service_id)
        args = service_parser.parse_args()
        for key, value in args.items():
            setattr(service, key, value)
        db.session.commit()
        return {'message': 'Service updated'}

# from serviceResources import ServiceResource, ServiceList

# def initialize_routes(api):
#     api.add_resource(ServiceList, '/services')  # GET all / POST new service
#     api.add_resource(ServiceResource, '/services/<int:service_id>')  # GET, DELETE, PUT for a single service
