from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView


class UserView(BrowserView):

    def __getitem__(self, key):
        return getToolByName(self.context, 'portal_membership').getMemberById(key)

    restrictedTraverse = __getitem__


class MemberDataDefaultView(BrowserView):

    def user_content(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        username = self.context.getId()
        if not username:
            return []
        query = {
            'Creator': username,
            'sort_on': 'created',
            'sort_order': 'reverse',
            'sort_limit': 10,
        }
        return catalog.searchResults(query)[:10]
