from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from z3c.formwidget.query.interfaces import IQuerySource
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from plone.principalsource.source import PrincipalSource
from plone.principalsource.source import PrincipalSourceBinder


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


class WorkspaceMemberSource(PrincipalSource):
    implements(IQuerySource)

    def __init__(self, context, users=True, groups=True, search_name=True):
        super(WorkspaceMemberSource, self).__init__(context, users, groups, search_name)
        self.root_users = self.context.getPhysicalRoot().acl_users

    def _searchPrincipals(self, *args, **kw):
        return (self.root_users.searchPrincipals(*args, **kw) +
                self.acl_users.searchPrincipals(*args, **kw))

    def _searchUsers(self, *args, **kw):
        return (self.root_users.searchUsers(*args, **kw) +
                self.acl_users.searchUsers(*args, **kw))

    def _searchGroups(self, *args, **kw):
        return (self.root_users.searchGroups(*args, **kw) +
                self.acl_users.searchGroups(*args, **kw))

    @property
    def _search(self):
        if self.users and self.groups:
            return self._searchPrincipals
        elif self.users:
            return self._searchUsers
        elif self.groups:
            return self._searchGroups

    def __iter__(self):
        seen = set()
        for result in self._search():
            if result['id'] not in seen:
                seen.add(result['id'])
                yield self._term_for_result(result)


class WorkspaceMemberSourceBinder(PrincipalSourceBinder):
    implements(IContextSourceBinder)

    def __call__(self, context):
        return WorkspaceMemberSource(context, self.users, self.groups)


WorkspaceMemberVocabularyFactory = WorkspaceMemberSourceBinder(groups=False)
