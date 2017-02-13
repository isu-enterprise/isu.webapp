# Web UI
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

from components import CreditSlip

class DefaultView(object):
    def __init__(self, model=None):
        self.model=None

class HomeView(DefaultView):
    title="ACME Interprise Platform"

@view_config(route_name='hello',
    renderer="complatform:admin-lte/index.pt")
def hello_world(request):
    return {"view":HomeView(),
        "request":request,
        "response":request.response}

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
    config.include('pyramid_chameleon')
    config.add_route('hello', '/')
    config.add_route('credit-slip', '/CS')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
