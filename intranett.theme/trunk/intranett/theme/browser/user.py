from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView


class UserView(BrowserView):

    def username(self):
        return self.request.form.get('name', '')

    def user_content(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {
            'Creator': self.username(),
            'sort_on': 'created',
            'sort_order': 'reverse',
            'sort_limit': 10,
        }
        return catalog.searchResults(query)[:10]
