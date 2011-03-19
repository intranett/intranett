from urllib import quote

from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize
from intranett.policy.utils import getMembersFolderId


class MemberDataView(BrowserView):
    """This is the user page view.
    """
    # XXX: The context of this view has a messed up acquisition chain.
    # XXX: Also see intranett.policy.tools.MemberData.

    @memoize
    def userid(self):
        return self.context.getId()

    @memoize
    def username(self):
        return self.context.getUserName()

    @memoize
    def userinfo(self):
        mt = getToolByName(self.context, 'portal_membership')
        return mt.getMemberInfo(self.userid())

    @memoize
    def userportrait(self):
        mt = getToolByName(self.context, 'portal_membership')
        return mt.getPersonalPortrait(self.userid(), thumbnail=False)

    @memoize
    def usercontent(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        userid = self.userid()
        if not userid: # pragma: no cover
            return []
        utils = getToolByName(self.context, 'plone_utils')
        search_types = utils.getUserFriendlyTypes()
        query = {
            'Creator': userid,
            'portal_type': search_types,
            'sort_on': 'created',
            'sort_order': 'reverse',
            'sort_limit': 10,
        }
        return catalog.searchResults(query)[:10]

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
