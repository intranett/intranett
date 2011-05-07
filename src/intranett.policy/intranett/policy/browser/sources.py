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


class PASFacade(object):
    """Query both Plone site and root user folder"""

    def __init__(self, plone_users):
        self.root_users = plone_users.getPhysicalRoot().acl_users
        self.plone_users = plone_users

    def getUserById(self, id):
        user = self.root_users.getUserById(id)
        if user is None:
            user = self.plone_users.getUserById(id)
        return user

    def getGroupById(self, id):
        group = self.root_users.getGroupById(id)
        if group is None:
            group = self.plone_users.getGroupById(id)
        return group

    def searchPrincipals(self, *args, **kw):
        return (self.root_users.searchPrincipals(*args, **kw) +
                self.plone_users.searchPrincipals(*args, **kw))

    def searchUsers(self, *args, **kw):
        return (self.root_users.searchUsers(*args, **kw) +
                self.plone_users.searchUsers(*args, **kw))

    def searchGroups(self, *args, **kw):
        return (self.root_users.searchGroups(*args, **kw) +
                self.plone_users.searchGroups(*args, **kw))


class WorkspaceMemberSource(PrincipalSource):
    implements(IQuerySource)

    @apply
    def acl_users():
        def get(self):
            return getattr(self, '_pas', None)
        def set(self, value):
            self._pas = None if value is None else PASFacade(value)
        return property(get, set)


class WorkspaceMemberSourceBinder(PrincipalSourceBinder):
    implements(IContextSourceBinder)

    def __call__(self, context):
        return WorkspaceMemberSource(context, self.users, self.groups)


WorkspaceMemberVocabularyFactory = WorkspaceMemberSourceBinder(groups=False)
