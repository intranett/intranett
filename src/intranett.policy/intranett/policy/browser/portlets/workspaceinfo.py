from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form as formlibform
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _


class IWorkspaceInfo(IPortletDataProvider):
    """Provides information such as members and visibility of a workspace"""


class Assignment(base.Assignment):

    implements(IWorkspaceInfo)

    title = _("Workspace Info")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('workspaceinfo.pt')

    @property
    def available(self):
        return (getattr(self.context, 'getWorkspace', None) is not None and
                'portal_factory' not in self.request.URL)

    @property
    def portletTitle(self):
        return _("Workspace Info")

    def update(self):
        if not self.available:
            return
        wf = getToolByName(self.context, 'portal_workflow')
        mt = getToolByName(self.context, 'portal_membership')
        ws = self.context.getWorkspace()
        self.state = wf.getInfoFor(ws, "workspace_visibility")
        self.title = ws.Title()
        members = sorted(ws.members)
        members = (mt.getMemberById(x) for x in members)
        self.members = tuple(x.getProperty("fullname") or x.getId() for x in members)


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)
