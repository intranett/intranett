from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.permissions import ManageUsers
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _


class IInvitePortlet(IPortletDataProvider):
    pass


class Assignment(base.Assignment):

    implements(IInvitePortlet)

    title = _("Invite others")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('invite.pt')
    portletTitle = _("Invite others")

    @property
    def available(self):
        return _checkPermission(ManageUsers, self.context)

    @memoize
    def invites(self):
        mt = getToolByName(self.context, 'portal_membership')
        it = getToolByName(self.context, 'portal_invitations')
        invites = it.getInvitesUser(sent=0, used=0)
        if not invites:
            # Auto-refresh number of allocated invites
            member = mt.getAuthenticatedMember()
            if 'Site Administrator' in member.getRoles():
                it.generateInvite(member.getId(), count=100)
                invites = it.getInvitesUser(sent=0, used=0)
        return not not invites


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
