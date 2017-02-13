# Web UI
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

from components import CreditSlip

@view_config(route_name='hello', renderer='string')
def hello_world(request):
    return 'Hello World'

@view_config(route_name="credit-slip", renderer="string")
def credit_slip_test(request):
    cs=CreditSlip(42)
    response=request.response
    #response.headerlist.append(("Content-Type","text/html"))
    return """
    <h1>Credit Slip Test</h1>
    <p>
    {}
    </p>""".format(cs)

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.add_route('credit-slip', '/CS')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
