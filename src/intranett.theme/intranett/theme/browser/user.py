from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from OFS.Traversable import _marker


class UserView(BrowserView):
    """This view pretends to be traversable so the catalog
    is able to reindex member data objects.
    """

    def __getitem__(self, key):
        return getToolByName(self.context, 'portal_membership').getMemberById(key)

    def unrestrictedTraverse(self, path, default=_marker, restricted=False):
        user = self[path]
        if user is None and default is not _marker:
            return default
        return user

    def restrictedTraverse(self, path, default=_marker):
        return self.unrestrictedTraverse(path, default)

    def getPhysicalPath(self):
        return self.context.getPhysicalPath() + ('user',)


class MemberDataView(BrowserView):

    def username(self):
        return self.context.getId()

    def user_content(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        username = self.username()
        if not username:
            return []
        query = {
            'Creator': username,
            'sort_on': 'created',
            'sort_order': 'reverse',
            'sort_limit': 10,
        }
        return catalog.searchResults(query)[:10]
