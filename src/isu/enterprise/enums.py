from zope.schema.interfaces import IVocabularyTokenized
from zope.schema.interfaces import ITokenizedTerm
from zope.interface import implementer, classImplements
from collections import namedtuple
from zope.schema.vocabulary import getVocabularyRegistry
#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory("isu.college")

EnumTerm = namedtuple('EnumItem', ['token', 'value'])
classImplements(EnumTerm, ITokenizedTerm)


@implementer(IVocabularyTokenized)
class Vocabulary(object):

    def __init__(self, enum):

        self.enum = enum
        self.terms = {item[1]: EnumTerm._make(item)
                      for item in enum.__members__.items()}
        enum.vocabulary = self

    def __call__(self, object):
        """Return myself as a factory execution result
        independent from content object
        """
        return self

    def __iter__(self):
        yield from self.terms.values()

    def __len__(self):
        return len(self.enum)

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
            value = self.enum.__members__[token]
            return self.terms[value]
        except KeyError:
            raise LookupError("wrong token")


class vocabulary(object):
    """Registers a vocabulary provider for a enum under
    name
    """

    def __init__(self, name=None):
        self.name = name

    def __call__(self, enum):
        """If a name was supplied then
        register the enum's vocabulary in
        global vocabulary registry
        """

        vocab = Vocabulary(enum)
        name = self.name
        if name is not None:
            registry = getVocabularyRegistry()
            registry.register(name, vocab)

        return enum
