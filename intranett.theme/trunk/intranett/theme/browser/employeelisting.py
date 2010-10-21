from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class EmployeeListingView(BrowserView):
    """Employee listing"""

    def employees(self):
        mt = getToolByName(self.context, 'portal_membership')
        members = mt.listMemberIds()
        member_info = [mt.getMemberInfo(member) for member in members]
        member_info.sort(key=lambda a:a['fullname'])
        return member_info