# Web UI module
# encoding: utf-8
from pyramid.config import Configurator
from isu.enterprise.configurator import createConfigurator
from zope.interface import directlyProvides
from isu.webapp.interfaces import IConfigurationEvent, IApplication
from isu.webapp.views import View
from zope.i18nmessageid import MessageFactory


_ = _N = MessageFactory("isu.webapp")


class HomeView(View):
    title = _N("ISU Enterprise Platform")


def hello_world(request):
    return {
        "view": HomeView(),
        "request": request,
        "response": request.response,
        "default": True,
    }


def main(global_config, **settings):
    # show_environment()
    config = Configurator(settings=settings)
    config.hook_zca()
    createConfigurator(global_config["__file__"],
                       registry=config.registry,
                       name="configuration")
    config.include('pyramid_zcml')
    config.load_zcml('isu.webapp:configure.zcml')
    config.include('pyramid_chameleon')

    directlyProvides(config, IConfigurationEvent)
    config.registry.notify(config)

    app = config.make_wsgi_app()
    config.registry.registerUtility(app, IApplication, name="application")
    config.registry.notify(app)

    return app


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(None)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
