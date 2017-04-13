# encoding:utf-8
from zope.interface import Interface, Attribute, implementer, directlyProvides
from zope.i18nmessageid import MessageFactory
import zope.schema

# Implementation - реализация
# Provide - обеспечить, **обслуживать**, оснащать.


_ = MessageFactory("isu.webapp")


class IConfigurationEvent(Interface):
    """Marker interface denoting a configurator
    instance to be the event.
    """
