from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form as formlibform
from zope.i18n import translate
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
        mtool = getToolByName(self.context, 'portal_membership')
        gtool = getToolByName(self.context, 'portal_groups')
        ws = self.context.getProjectRoom()
        self.state = ws.getProjectRoomState()
        self.title = ws.Title()
        result = []
        for name in ws.participants:
            if name == 'AuthenticatedUsers':
                name = translate(u'Authenticated Users (Virtual Group)',
                    domain='plone', context=self.request)
                result.append(name)
                continue
            member = mtool.getMemberById(name)
            if member is not None:
                name = member.getProperty("fullname") or name
            else:
                group = gtool.getGroupById(name)
                if group is not None:
                    name = group.getProperty('title') or name
            result.append(name)
        self.participants = tuple(result)


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IProjectRoomInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IProjectRoomInfo)
