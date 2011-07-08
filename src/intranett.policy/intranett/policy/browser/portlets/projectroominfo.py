from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form as formlibform
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _


class IProjectRoomInfo(IPortletDataProvider):
    pass


class Assignment(base.Assignment):

    implements(IProjectRoomInfo)
    title = _("Project Info")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('projectroominfo.pt')

    @property
    def available(self):
        return (getattr(self.context, 'getProjectRoom', None) is not None and
                'portal_factory' not in self.request.URL)

    def update(self):
        if not self.available:
            return
        mt = getToolByName(self.context, 'portal_membership')
        ws = self.context.getProjectRoom()
        self.state = ws.getProjectRoomState()
        self.title = ws.Title()
        self.members = tuple(x.getProperty("fullname") or x.getId()
            for x in (mt.getMemberById(x) for x in ws.members))


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IProjectRoomInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IProjectRoomInfo)
