from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form as formlibform
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _


class IMyWorkspaces(IPortletDataProvider):
    """Provides a list of all of my workspaces"""


class Assignment(base.Assignment):

    implements(IMyWorkspaces)

    title = _("My Workspaces")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('myworkspaces.pt')

    @property
    def available(self):
        return True

    @property
    def portletTitle(self):
        return _("My Workspaces")

    def update(self):
        if not self.available:
            return
        ct = getToolByName(self.context, 'portal_catalog')
        user_id = getSecurityManager().getUser().getId()
        self.workspaces = ({'title':x.Title, 'url':x.getURL()} for x in
            ct(portal_type="TeamWorkspace", workspaceMembers=(user_id,)))


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IMyWorkspaces)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IMyWorkspaces)
