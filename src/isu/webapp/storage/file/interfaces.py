from zope.interface import Interface, Attribute
from isu.webapp.storage.interfaces import IStorageView


class IFile(Interface):
    name = Attribute("Full name of the file")
    ext = Attribute('Extension part of the file, without the first dot')
    base_name = Attribute("Base name of the file, i.e. name without extension")
    mime_type = Attribute("Mime type of the file")
    key = Attribute("Key identifier of the file")
    content = Attribute("Content of the file, bytes")

    def set_content(content):
        """Sets content and other its characteristics"""


class IFileStorage(Interface):
    def store(file):
        """Stores file in the storage"""

    def files(filter):
        """Returns file list filtered somehow by `filter` """

    def set_session(session):
        """Informs receiver on the current session """
        # TODO: It is redundant

    def load(key):
        """Load IFile object by its key,
        raises KeyError, if there is no such key"""


class IFileStorageView(IStorageView):
    """Interface for File Objects Storage """

    def files(filter):
        """Returns list of files as a text or json,
        it depends on the view setup"""

    def upload():
        """Processes file post command"""

    def form():
        """Form render helper"""

    def on_upload(file):
        """Run by upload after file object extraction"""
