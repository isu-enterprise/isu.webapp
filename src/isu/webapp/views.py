from zope.interface import implementer
from .interfaces import IView
from zope.component import getUtility
import pyramid.threadlocal
#import uuid

# GSM = getSiteManager()


# def UUID():
#    return str(uuid.uuid1())


# @implementer(IViewRegistry)
# class ViewRegistry(object):
#     """
#     Registers views under a non-empty name.
#     """

#     def __init__(self):
#         self.views = {}

#     def register(self, view, name):
#         """
#         Register a view under a name
#         """
#         self.views[name] = view

#     def get(self, name, default=None):
#         return self.views.get(name, default)

#     def unregister(self, name):
#         if name in self.views:
#             del self.views[name]


# view_registry = ViewRegistry()

# GSM.registerUtility(view_registry)


@implementer(IView)
class View(object):

    def __init__(self, context=None, request=None):
        self.context = context
        self._request = request

    @property
    def registry(self):
        if self._request is not None:
            return self._request.registry
        else:
            return pyramid.threadlocal.get_current_registry()

    @property
    def request(self):
        if self._request is not None:
            return self._request
        else:
            return pyramid.threadlocal.get_current_request()

    # @property
    # def uuid(self):
    #     if not hasattr(self, "__uuid__"):
    #         self.__uuid__ = UUID()
    #         view_registry = getUtility(IViewRegistry)
    #         view_registry.register(self, self.__uuid__)
    #     return self.__uuid__
