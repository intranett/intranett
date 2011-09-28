from AccessControl import getSecurityManager
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
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
    available = True


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
