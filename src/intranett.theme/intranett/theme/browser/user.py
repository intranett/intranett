from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize


class MemberDataView(BrowserView):
    """This is the user page view.
    """
    # XXX: The context of this view has a messed up acquisition chain.
    # XXX: Also see intranett.policy.tools.MemberData.

    @memoize
    def username(self):
        return self.context.getId()

    @memoize
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
