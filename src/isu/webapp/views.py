from zope.interface import implementer
from .interfaces import IView, IViewRegistry, IPanelItem
import pyramid.threadlocal
import uuid

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("icc.quest")


def UUID():
    return str(uuid.uuid1())


@implementer(IPanelItem)
class PanelItem(object):
    def __init__(self, name, URL=None, route=None, icon=None):
        if route is None and URL is None:
            raise ValueError('either URL or route parameter must be specified')
        self.name = name
        self._URL = URL
        self.route = route
        self.icon = icon

    def URL(self, request=None):
        if self._URL is not None:
            return self._URL
        else:
            return request.route_url(self.route)

    def active(self, request):
        if self.route is not None:
            return 'active' if request.matched_route.name == self.route else ''
        return 'active' if request.url == self._URL else ''

    # TODO: Implement treeview class support in index.pt


@implementer(IView)
class View(object):
    """Adapter object of context (a model) and request
    (a browser query) to a template.
    """

    def __init__(self, context=None, request=None):
        """Initializes the view as being adapter of
        `context`, being a model, and
        `request`, being a object reflecting query from client,
        to a template.
        """
        self.context = context
        self._request = request

    @property
    def registry(self):
        """Registry property aoopted for testing."""
        if self._request is not None:
            return self._request.registry
        else:
            return pyramid.threadlocal.get_current_registry()

    @property
    def request(self):
        """Request property, which is taken either from request
        or from thread local context to support testing.
        """
        if self._request is not None:
            return self._request
        else:
            return pyramid.threadlocal.get_current_request()

    def response(self, **kwargs):
        """Returns a dictionary of standard varibales.
        `kwargs`: additional variables to be added.
        """
        resp = {
            'view': self,
            'context': self.context,
            'request': self.request
        }
        resp.update(kwargs)
        return resp


class MarkedView(View):
    @property
    def uuid(self):
        if not hasattr(self, "__uuid__"):
            self.__uuid__ = UUID()
            view_registry = self.registry.getUtility(IViewRegistry)
            view_registry.register(self, self.__uuid__)
        return self.__uuid__


@implementer(IViewRegistry)
class ViewRegistry(object):
    """
    Registers views under a non-empty name.
    """

    def __init__(self):
        self.views = {}

    def register(self, view, name):
        """
        Register a view under a name
        """
        self.views[name] = view

    def get(self, name, default=None):
        return self.views.get(name, default)

    def unregister(self, name):
        if name in self.views:
            del self.views[name]
