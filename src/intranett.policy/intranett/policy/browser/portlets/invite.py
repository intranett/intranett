from AccessControl import getSecurityManager
from plone.memoize.view import memoize
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.permissions import ManageUsers
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
        inv_tool = getToolByName(self.context, 'portal_invitations')
        return inv_tool.getInvitesUser(sent=0, used=0)


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
