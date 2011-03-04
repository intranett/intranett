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

    def documents(self, text=None):
        sr = getUtility(ISiteRoot)
        catalog = getToolByName(sr, 'portal_catalog')
        query = {'portal_type': ['Document', 'Event', 'News Item', 'Link'],
            'review_state': 'published', 'sort_limit': 10}
        if text is not None:
            query['Title'] = text
        return catalog.unrestrictedSearchResults(query)

    @property
    def vocab(self):
        return SimpleVocabulary.fromItems(
            [(doc.Title, doc.UID) for doc in self.documents()])

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
        return [self.getTerm(doc.UID)
                for doc in self.documents(text=query_string.lower() + '*')]


class DocumentSourceBinder(object):
    implements(IContextSourceBinder)

    def __call__(self, context):
        return DocumentSource(context)
