# encoding:utf-8
from zope.interface import Interface, Attribute
import zope.schema

# Implementation - реализация
# Provide - обеспечить, **обслуживать**, оснащать.

def _N(x):
    return x

class IAccountingEntry(Interface):
    cr=Attribute("Credit account")
    dr=Attribute("Debit account")
    amount=Attribute("Amount of money sent")
    currency=Attribute("A currency id")
    moment=Attribute("A DateTime moment of the entry")

class IDocument(Interface):
    def create():
        """
        Create document.
        """
    def delete():
        """
        Delete the document.
        """
    def save():
        """
        Store the document in a global storage,
        and create a set of accounting entries.
        """

class ICreditSlip(IDocument):
    """Приходный ордер
    """

    reason=zope.schema.TextLine(\
        title=_N(u"Reason"),
        description=_N(u"The reason of the peration to be conducted."),
        required = True
        )

    def addentry(entry):
        """
        Adds an accounting
        entry in the credit slip.
        """

class IStorage(Interface):
    def store(document):
        """
        Store the document in storage
        """

class IStorable(Interface):
    """Interface for description
    methods, which save and loads data
    for adaptee objects.
    """
    def store_into(storage):
        """Store data of adapted component
        into the storage
        """

class IConfigurator(Interface):
    """Interface defines an object, which
    is a configurator of platform.
    """
