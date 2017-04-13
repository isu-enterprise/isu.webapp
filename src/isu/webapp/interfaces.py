# encoding:utf-8
from zope.interface import Interface, Attribute, implementer, directlyProvides
from zope.i18nmessageid import MessageFactory
import zope.schema
import enum  # FIXME: Оформит словари в отделный подмодуль.

# Implementation - реализация
# Provide - обеспечить, **обслуживать**, оснащать.


_ = MessageFactory("isu.webapp")


class IAccountingEntry(Interface):
    cr = Attribute("Credit account")
    dr = Attribute("Debit account")
    amount = Attribute("Amount of money sent")
    currency = Attribute("A currency id")
    moment = Attribute("A DateTime moment of the entry")


class IncludingEnum(enum.Enum):
    with_VAT = 1
    without_VAT = 0


directlyProvides(IncludingEnum,
                 zope.schema.interfaces.IBaseVocabulary)


class IDocument(Interface):
    number = zope.schema.TextLine(
        title=_("Number"),
        description=_("The number of the document,"
                      "usually an unique member of some"
                      "sequence."),
        required=True,
        # readonly=True,
        # order=0
    )

    date = zope.schema.Datetime(
        title=_("Дата"),
        description=_("Дата проведения документа."),
        readonly=True,
        # order=1,
        required=True
    )

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

    reason = zope.schema.TextLine(
        title=_(u"Reason"),
        description=_(u"The reason of the peration to be conducted."),
        required=True,
    )

    contractor = zope.schema.TextLine(
        title=_(u"Contractor"),
        description=_(u"The contractor giving money."),
        required=True
        #validator=lambda x: x.strip()
    )

    including = zope.schema.Choice(
        title=_(u"Including"),
        description=_(
            u"The additional circunstances accompanying the document."),
        required=True,
        vocabulary=IncludingEnum
    )
    #~ including = zope.schema.TextLine(
    #~ title=_(u"Including"),
    #~ description=_(u"The additional circunstances accompanying the document."),
    #~ required=False
    #~ )

    appendix = zope.schema.TextLine(
        title=_(u"Appendix"),
        description=_(u"The appendix of the document."),
        required=False
    )

    entries = zope.schema.List(
        title=_(u"Entries"),
        description=_(u"The entry list providing the credit slip"),
        required=True
    )

    def addentry(entry):
        """
        Adds an accounting
        entry in the credit slip.
        """


class IContractor(Interface):
    """The interface describes a person or
    company that undertakes a contract
    to provide materials or labor
    to perform a service or do a job.
    -- (c) Google
    """
    name = zope.schema.TextLine(
        title=_(u"name"),
        description=_(u"Name of the contractor."),
        required=True
    )


class IOrganization(IContractor):
    """
    """


class ISubdivision(IOrganization):
    pass


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
