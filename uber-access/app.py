from wsgiref.simple_server import make_server
from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.response import Response
from uber_access import UberAccess

# Ended up with Pyramid Framework since it seems may be the simplest, idk we'll see

@view_config(route_name='available_products', renderer='json',
             request_method='POST')
def get_available_products(request):
    data = request.json_body['data']
    lat = data['lat']
    long = data['long']
    ub_instance = UberAccess()
    response = ub_instance.get_price_estimates(lat, long)
    # TODO: FORMAT RESPONSE to print out needed data
    return response

@view_config(route_name='available_products', renderer='json',
             request_method='POST')
def get_price_estimate(request):
    data = request.json_body['data']
    ub_instance = UberAccess()
    response = ub_instance.get_price_estimates(start_lat= data['start_lat'], start_long=data['start_long'], end_lat=data['end_lat'],
                                    end_long=data['end_long'], seat_count=data['seat_count'])
    # TODO: Format response to whats needed
    return response

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('price_estimate', '/price_estimate')
        config.add_view(get_price_estimate, route_name='price_estimate')
        config.add_route('available_products', '/available_products')
        config.add_view(get_available_products, route_name='available_products')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    server.serve_forever()