# Web UI module
# encoding: utf-8
from pyramid.config import Configurator
from pyramid.view import view_config

from icc.mvw.interfaces import IView, IViewRegistry
from isu.enterprise.interfaces import ICreditSlip
from isu.onece.interfaces import IVocabularyItem
from zope.interface import implementer, directlyProvides
from zope.component import (
    adapter,
    getGlobalSiteManager,
    createObject,
    getUtility,
    queryUtility,
    handle
)

from isu.enterprise.components import CreditSlip
from isu.enterprise.configurator import createConfigurator


from isu.onece.org.components import Commondities
from isu.onece.interfaces import IVocabularyItem, IVocabulary

from isu.webapp.interfaces import IConfigurationEvent
import configparser

import collections
import uuid

conf = createConfigurator("development.ini")

try:
    module = conf["app:main"]["routes"]
    # FIXME: DNU (Do not understand)  why 'egg:'?
    import importlib
    module = module.lstrip("egg:")
    importlib.import_module(module)
except configparser.NoSectionError:
    pass


def UUID():
    return str(uuid.uuid1())


def _N(x):
    return x


GSM = getGlobalSiteManager()

_default = object()


class HomeView(DefaultView):
    title = _N("ISU Enterprise Platform")


@view_config(route_name='home', renderer="isu.webapp:templates/index.pt")
def hello_world(request):
    return {
        "view": HomeView(),
        "request": request,
        "response": request.response,
        "default": True,
    }


@adapter(ICreditSlip)
class CreditSlipView(DefaultView):
    title = _N("Credit Slip")
    body = "<strong>11111</strong>"
    style_css = """"""

    @property
    def date(self):
        return str(self.context.date).split(" ")[0]


@adapter(IVocabulary)
class VocabularyEditorView(DefaultView):
    title = _N("Vocabulary editor")

    def __init__(self, context=None):
        self.context = context
        self.uuids = collections.OrderedDict()

    @property
    def terms(self):
        return self.context.terms

    def termuuid(self, term=None):
        if term is None:
            return super(VocabularyEditorView, self).uuid()

        if term in self.uuids:
            return self.uuids[term]
        else:
            uuid_ = UUID()
            return self.uuids.setdefault(term, uuid_)


GSM.registerAdapter(VocabularyEditorView)


@view_config(route_name="credit-slip", renderer="isu.webapp:templates/credit-slip.pt")
def credit_slip_test(request):
    cs = CreditSlip(42, reason="Зарплата директору")
    # response = request.response
    # response.headerlist.append(("Content-Type","text/html"))
    view = CreditSlipView(cs)
    return {
        "view": view,
        "request": request,
        "response": request.response,
        "context": cs,
        "default": True
    }


@view_config(route_name="vocabulary-editor",
             renderer="isu.webapp:templates/vocabulary-editor.pt")
def vocabulary_editor(request):
    vocab = Commondities(factory_name='commondity')
    vocab.append(createObject('commondity', 10, "Air"))
    vocab.append(createObject('commondity', 23, "Water"))
    vocab.append(createObject('commondity', 34, "Soil"))
    vocab.append(createObject('commondity', 42, "Fire"))
    vocab.append(createObject('commondity', 54, "Star"))
    view = IView(vocab)
    return {
        "view": view,
        "request": request,
        "response": request.response,
        "context": vocab,
        "default": True
    }


@view_config(route_name="vocabulary-editor-api-save",
             renderer="json",
             request_method="POST"
             )
def vocabulary_editor_api_save(request):
    query = request.json_body
    view_uuid = query["uuid"]
    view_registry = getUtility(IViewRegistry)
    view = view_registry.get(view_uuid, None)
    if view is None:
        return {"status": "KO", "message": "Cannot find view associated with the session!"}
    context = vocab = view.context
    print(context)
    return {"status": "OK", "message": _N("Changes saved!")}


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_zcml')
    # config.load_zcml('isu.webapp:configure.zcml')
    config.include('pyramid_chameleon')
    # Static assets configuration
    config.add_static_view(
        name='bootstrap', path='isu.webapp:admin-lte/bootstrap')
    config.add_static_view(name='documentation',
                           path='isu.webapp:admin-lte/documentation')
    config.add_static_view(name='pages', path='isu.webapp:admin-lte/pages')
    config.add_static_view(
        name='plugins', path='isu.webapp:admin-lte/plugins')
    config.add_static_view(name='dist', path='isu.webapp:admin-lte/dist')
    config.add_static_view(name='js', path='isu.webapp:templates/js')
    # End of static assets
    config.add_route('home', '/')
    config.add_route('credit-slip', '/CS')
    config.add_route('vocabulary-editor', '/VE')
    config.add_route('vocabulary-editor-api-save', '/VE/api/save')
    config.add_subscriber('isu.webapp.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    config.scan()

    directlyProvides(config, IConfigurationEvent)
    handle(config)
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(None)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
