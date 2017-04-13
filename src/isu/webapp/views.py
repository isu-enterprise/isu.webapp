from zope.interface import implementer
from icc.mvw.interfaces import IView, IViewRegistry
from zope.component import getGlobalSiteManager

GSM = getGlobalSiteManager()


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


view_registry = ViewRegistry()

GSM.registerUtility(view_registry)


@implementer(IView)
class DefaultView(object):

    def __init__(self, context=None):
        self.context = context

    @property
    def uuid(self):
        if not hasattr(self, "__uuid__"):
            self.__uuid__ = UUID()
            view_registry = getUtility(IViewRegistry)
            view_registry.register(self, self.__uuid__)
        return self.__uuid__
