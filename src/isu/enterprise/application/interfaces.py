from zope.interface import Interface, Attribute
# import zope.schema


class IApplication(Interface):
    """Defines an application object,
    which could be only one, i.e., utility.
    """

    name = Attribute("Name of the application")
    category = Attribute("Category name of the application")
    vendor = Attribute("Vendor of the application")

    def run():
        """Runs the application, e.g., starts the event loop
        """
