from .interfaces import IStorageView
from zope.interface import implementer
from isu.webapp.views import View

@implementer(IStorageView)
class StorageView(View):
    def objects(self, filter=None):
        """Returns a list of objects uploaded and stored,
        `filter` defines a filtering param in some way"""
        raise RuntimeError('Not implemented yet. Any suggestions?')

    def upload(self):
        raise RuntimeError('Not implemented yet. Any suggestions?')

    def form(self):
        return self.response()

