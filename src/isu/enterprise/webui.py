# Web UI module
# encoding: utf-8
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

from icc.mvw.interfaces import IView
from isu.enterprise.interfaces import ICreditSlip
from isu.onece.interfaces import IVocabularyItem
from zope.interface import implementer
from zope.component import adapter, getGlobalSiteManager, createObject

from isu.enterprise.components import CreditSlip
from isu.enterprise.configurator import createConfigurator


from isu.onece.org.components import Commondities
from isu.onece.interfaces import IVocabularyItem, IVocabulary

import collections
import uuid

createConfigurator("development.ini")


def _N(x):
    return x


GSM = getGlobalSiteManager()


@implementer(IView)
class DefaultView(object):

    def __init__(self, context=None):
        self.context = context

    @property
    def uuid(self):
        if not hasattr(self, "__uuid__"):
            self.__uuid__ = uuid.uuid1()
            print(self.__uuid__, type(self.__uuid__))
            GSM.registerUtility(self, name=str(self.__uuid__))
        return self.__uuid__


class HomeView(DefaultView):
    title = _N("ISU Enterprise Platform")


@view_config(route_name='home', renderer="isu.enterprise:templates/index.pt")
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
            uuid_ = uuid.uuid1()
            return self.uuids.setdefault(term, uuid_)

GSM.registerAdapter(VocabularyEditorView)


@view_config(route_name="credit-slip", renderer="isu.enterprise:templates/credit-slip.pt")
def credit_slip_test(request):
    cs = CreditSlip(42, reason="Зарплата директору")
    #response = request.response
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
             renderer="isu.enterprise:templates/vocabulary-editor.pt")
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
    return {"status":"OK", "message":_N("Changes saved!")}


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_zcml')
    #config.load_zcml('isu.enterprise:configure.zcml')
    config.include('pyramid_chameleon')
    # Static assets configuration
    config.add_static_view(
        name='bootstrap', path='isu.enterprise:admin-lte/bootstrap')
    config.add_static_view(name='documentation',
                           path='isu.enterprise:admin-lte/documentation')
    config.add_static_view(name='pages', path='isu.enterprise:admin-lte/pages')
    config.add_static_view(
        name='plugins', path='isu.enterprise:admin-lte/plugins')
    config.add_static_view(name='dist', path='isu.enterprise:admin-lte/dist')
    config.add_static_view(name='js', path='isu.enterprise:templates/js')
    # End of static assets
    config.add_route('home', '/')
    config.add_route('credit-slip', '/CS')
    config.add_route('vocabulary-editor', '/VE')
    config.add_route('vocabulary-editor-api-save', '/VE/api/save')
    config.add_subscriber('isu.enterprise.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    config.scan()
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main(None)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
