# encoding:utf-8
from zope.interface import Interface, Attribute, implementer, directlyProvides
from zope.i18nmessageid import MessageFactory
import icc.mvw.interfaces
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

    cobtext = Attribute("The context object")
    request = Attribute("The request object")
    registry = Attribute("The registry of the application")

    # FIXME: add title, menu item, etc.
