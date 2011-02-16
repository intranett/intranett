from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from z3c.formwidget.query.interfaces import IQuerySource
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


class DocumentSource(object):
    implements(IQuerySource)

    def __init__(self, context):
        self.context = context

    @property
    def documents(self):
        """ XXX: Should be cached somehow.
        """
        sr = getUtility(ISiteRoot)
        catalog = getToolByName(sr, 'portal_catalog')
        return catalog.unrestrictedSearchResults(portal_type="Document",
            review_state='published')

    @property
    def vocab(self):
        return SimpleVocabulary.fromItems(
            [(doc.Title, doc.UID) for  doc in self.documents])

    def __contains__(self, term):
        return self.vocab.__contains__(term)

    def __iter__(self):
        return self.vocab.__iter__()

    def __len__(self):
        return self.vocab.__len__()

    def getTerm(self, value):
        return self.vocab.getTerm(value)

    def getTermByToken(self, value):
        return self.vocab.getTermByToken(value)

    def search(self, query_string):
        q = query_string.lower()
        return [self.getTerm(doc.UID)
                for doc in self.documents
                if q in doc.Title.lower()]


class DocumentSourceBinder(object):
    implements(IContextSourceBinder)

    def __call__(self, context):
        return DocumentSource(context)
