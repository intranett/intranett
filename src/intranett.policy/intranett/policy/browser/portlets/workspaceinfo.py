from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form as formlibform
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _


class IWorkspaceInfo(IPortletDataProvider):
    pass


class Assignment(base.Assignment):

    implements(IWorkspaceInfo)

    title = _("Project Info")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('workspaceinfo.pt')

    @property
    def available(self):
        return (getattr(self.context, 'getWorkspace', None) is not None and
                'portal_factory' not in self.request.URL)

    def update(self):
        if not self.available:
            return
        mt = getToolByName(self.context, 'portal_membership')
        ws = self.context.getWorkspace()
        self.state = ws.getWorkspaceState()
        self.title = ws.Title()
        self.members = tuple(x.getProperty("fullname") or x.getId()
            for x in (mt.getMemberById(x) for x in ws.members))


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)
