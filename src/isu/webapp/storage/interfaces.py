from isu.webapp.interfaces import IView

class IStorageView(IView):
    """A view with object storage functionality"""

    def upload():
        """Recives request with upload request"""

    def objects(filter):
        """Returns list of objects with filter applied"""

    def form():
        """Helper method for form rendering"""
