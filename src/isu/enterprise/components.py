from isu.enterprise.interfaces import IAccountingEntry, IDocument, IStorage, ICreditSlip
from zope.interface import implementer
import datetime

# Implementation.
RUB = 643
EUR = 810


@implementer(IAccountingEntry)
class Entry(object):
    def __init__(self, cr, dr, amount, currency=None, moment=None):
        self.cr = cr
        self.dr = dr
        self.amount = amount
        if currency is None:
            currency = RUB
        self.currency = currency
        if moment is None:
            self.moment = datetime.datetime.utcnow()


@implementer(IDocument)
class Document(object):
    def __init__(self, number, date=None):
        self.number = number
        if date is None:
            date = datetime.datetime.utcnow()
        self.date = date


@implementer(ICreditSlip)
class CreditSlip(Document):
    def __init__(self, number, date=None):
        super(CreditSlip, self).__init__(number, date=None)
        self.entries = []
        self.reason = ''
        self.contractor= ''
        self.including = ''
        self.appendix  = ''

    def addentry(self, entry):
        self.entries.append(entry)
