from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class EmployeeListingView(BrowserView):
    """Employee listing"""

    def __init__(self, context, request):
#        import pdb; pdb.set_trace( )
        super(EmployeeListingView, self).__init__(context, request)
        mt = getToolByName(self.context, 'portal_membership')
        md = getToolByName(self.context, 'portal_memberdata')
        members = mt.listMemberIds()
        self.member_info = []
        self.departments = set()
        for member in members:
            info = mt.getMemberInfo(member)
            if md.portraits.has_key(member):
                info['portrait_url'] = "%s/portraits/%s" % (md.absolute_url(), member)
                info['thumbnail_url'] = "%s/thumbnails/%s" % (md.absolute_url(), member)
            self.member_info.append(info)
            if info['department']:
                self.departments.add(info['department'])

        self.member_info.sort(key=lambda a:a['fullname'])
        self.departments = list(self.departments)
        self.departments.sort()

    def departments(self):
        return self.departments

    def employees(self, department=''):
        if department:
            return [info
                    for info in self.member_info
                    if info['department'] == department]
        return self.member_info
