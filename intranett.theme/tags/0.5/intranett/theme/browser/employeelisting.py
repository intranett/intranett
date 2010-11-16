from operator import itemgetter

from zope.publisher.browser import BrowserView
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName


class EmployeeListingView(BrowserView):
    """Employee listing"""

    def update(self):
        mt = getToolByName(self.context, 'portal_membership')
        md = getToolByName(self.context, 'portal_memberdata')
        members = mt.listMemberIds()
        self.member_info = []
        self.department_info = set()
        for member in members:
            info = mt.getMemberInfo(member)
            if member in md.portraits:
                md_url = md.absolute_url()
                info['portrait_url'] = "%s/portraits/%s" % (md_url, member)
                info['thumbnail_url'] = "%s/thumbnails/%s" % (md_url, member)
            else:
                info['portrait_url'] = ''
                info['thumbnail_url'] = ''
            self.member_info.append(info)
            if info['department']:
                self.department_info.add(info['department'])

        self.member_info.sort(key=itemgetter('fullname'))
        self.department_info = list(self.department_info)
        self.department_info.sort()

    def can_manage(self):
        sm = getSecurityManager()
        return sm.checkPermission('Manage users', aq_inner(self.context))

    def departments(self):
        return self.department_info

    def employees(self, department=''):
        if department:
            return [info
                    for info in self.member_info
                    if info['department'] == department]
        return self.member_info
