from zope.schema.interfaces import IVocabularyTokenized
from zope.schema.interfaces import ITokenizedTerm
from zope.interface import implementer, classImplements
from collections import namedtuple
#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory("isu.college")

EnumTerm = namedtuple('EnumItem', ['token', 'value'])
classImplements(EnumTerm, ITokenizedTerm)


@implementer(IVocabularyTokenized)
class vocabulary(object):

    def __init__(self, context):
        self.context = context
        self.terms = {item[1]: EnumTerm._make(item)
                      for item in context.__members__.items()}

    def __iter__(self):
        yield from self.terms.values()

    def __len__(self):
        return len(self.context)

    def getTerm(self, value):
        try:
            return self.terms[value]
        except KeyError:
            raise LookupError("wrong value")

    def __getitem__(self, value):
        return self.getTerm(value)

    def __contains__(self, value):
        return value in self.terms

    def getTermByToken(self, token):
        try:
            value = self.context.__members__[token]
            return self.terms[value]
        except KeyError:
            raise LookupError("wrong token")
