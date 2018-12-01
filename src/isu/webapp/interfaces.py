# encoding:utf-8
from zope.interface import Interface, Attribute, implementer, directlyProvides
from zope.i18nmessageid import MessageFactory
import icc.mvw.interfaces
import isu.enterprise.interfaces
import zope.schema

# Implementation - реализация
# Provide - обеспечить, **обслуживать**, оснащать.


_ = MessageFactory("isu.webapp")


class IConfigurationEvent(Interface):
    """Marker interface denoting a configurator
    instance to be the event.
    """


class IView(icc.mvw.interfaces.IView):
    """Defines Pyramid application view being
    an adapter of context and request object
    to a response
    """

    context = Attribute("The context object")
    request = Attribute("The request object")
    registry = Attribute("The registry of the application")
    title = Attribute("Title of the View")  # are to be implemented

    def response(**kwargs):
        """Returns a dictionary of standard varibales.
        `kwargs`: additional variables to be added.
        """

    # FIXME: menu item, etc.


class IViewRegistry(Interface):
    """Interface of a marked view registry"""

    def register(view, name):
        """Register the `view` instance under a `name`."""

    def get(name, default=None):
        """Find the `view` by its `name`.
        Return `default`  value if none found."""

    def unregister(name):
        """Remove registration defined by `name`."""


class IApplication (isu.enterprise.interfaces.IApplication):
    pass


class IPanelItem(Interface):
    name = Attribute("Item name")
    URL = Attribute("Absolute URL of the item page")
    route = Attribute("Route name of the item page")
    icon = Attribute("Name of an icon specification, e.g., 'fa fa-edit' ")
