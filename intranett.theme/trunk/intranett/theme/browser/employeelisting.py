from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class EmployeeListingView(BrowserView):
    """Employee listing"""

    def __init__(self, context, request):
        super(EmployeeListingView, self).__init__(context, request)
        mt = getToolByName(self.context, 'portal_membership')
        md = getToolByName(self.context, 'portal_memberdata')
        members = mt.listMemberIds()
        self.member_info = []
        self.department_info = set()
        for member in members:
            info = mt.getMemberInfo(member)
            if member in md.portraits:
                info['portrait_url'] = "%s/portraits/%s" % (md.absolute_url(), member)
                info['thumbnail_url'] = "%s/thumbnails/%s" % (md.absolute_url(), member)
            else:
                info['portrait_url'] = ''
                info['thumbnail_url'] = ''
            self.member_info.append(info)
            if info['department']:
                self.department_info.add(info['department'])

        self.member_info.sort(key=lambda a:a['fullname'])
        self.department_info = list(self.department_info)
        self.department_info.sort()

    def departments(self):
        return self.department_info

    def employees(self, department=''):
        if department:
            return [info
                    for info in self.member_info
                    if info['department'] == department]
        return self.member_info
