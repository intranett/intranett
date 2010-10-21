from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class EmployeeListingView(BrowserView):
    """Employee listing"""

    def employees(self):
        pass
