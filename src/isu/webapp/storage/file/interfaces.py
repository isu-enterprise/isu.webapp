from zope.interface import Interface
from isu.webapp.storage.interfaces import IStorageView



class IFileStorageView(IStorageView):
    """Interface for File Objects Storage """

    def files(filter):
        """Returns list of files as a text or json,
        it depends on the view setup"""