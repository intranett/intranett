from operator import itemgetter
from urllib import quote

from zope.publisher.browser import BrowserView
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize
from intranett.policy.utils import getMembersFolderId


class UsersListingView(BrowserView):
    """Users listing"""

    def update(self):
        mt = getToolByName(self.context, 'portal_membership')
        md = getToolByName(self.context, 'portal_memberdata')
        self.member_info = []
        self.department_info = {}
        for member_id in mt.listMemberIds():
            info = mt.getMemberInfo(member_id)
            info['url'] = self.user_url(member_id)
            info['portrait_url'] = ''
            info['thumbnail_url'] = ''
            info['department_url'] = ''
            info['review_state'] = 'published' # Fake
            if member_id in md.portraits:
                info['portrait_url'] = self.portrait_url(member_id)
                info['thumbnail_url'] = self.thumbnail_url(member_id)
            if 'department' in info and info['department']:
                info['department_url'] = self.department_url(info['department'])
                self.department_info.setdefault(info['department'], {
                    'name': info['department'],
                    'url': info['department_url']
                    })
            self.member_info.append(info)

        self.member_info.sort(key=itemgetter('fullname'))
        self.department_info = self.department_info.values()
        self.department_info.sort(key=itemgetter('name'))

    def can_manage(self):
        sm = getSecurityManager()
        return sm.checkPermission('Manage users', aq_inner(self.context))

    def departments(self):
        return self.department_info

    def users(self, department=''):
        if department:
            return [info
                    for info in self.member_info
                    if info['department'] == department]
        return self.member_info

    @memoize
    def portrait_url(self, member_id):
        md = getToolByName(self.context, 'portal_memberdata')
        return md.absolute_url() + '/portraits/' + quote(member_id)

    @memoize
    def thumbnail_url(self, member_id):
        md = getToolByName(self.context, 'portal_memberdata')
        return md.absolute_url() + '/thumbnails/' + quote(member_id)

    @memoize
    def user_url(self, member_id):
        return self.users_folder_url() + '/' + quote(member_id)

    @memoize
    def department_url(self, department):
        return self.users_folder_url() + '?department=' + quote(department)

    @memoize
    def users_folder_url(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return portal.absolute_url() + '/' + quote(getMembersFolderId())
