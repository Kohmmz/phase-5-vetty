from serviceResources import ServiceResource, ServiceList

def initialize_routes(api):
    api.add_resource(ServiceList, '/services')  # GET all / POST new service
    api.add_resource(ServiceResource, '/services/<int:service_id>')  # GET, DELETE, PUT for a single service
