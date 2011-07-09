from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form as formlibform
from zope.i18n import translate
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _
from intranett.policy.utils import get_user_profile_url


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
        context = self.context
        mtool = getToolByName(context, 'portal_membership')
        gtool = getToolByName(context, 'portal_groups')
        room = self.context.getProjectRoom()
        self.state = room.getProjectRoomState()
        self.title = room.Title()
        self.project_url = room.absolute_url()
        result = []
        for name in room.participants:
            title = name
            url = None
            if name == 'AuthenticatedUsers':
                title = translate(u'Authenticated Users (Virtual Group)',
                    domain='plone', context=self.request)
                result.append(dict(name=name, title=title, url=None))
                continue
            member = mtool.getMemberById(name)
            if member is not None:
                title = member.getProperty("fullname") or name
                url = get_user_profile_url(context, name)
            else:
                group = gtool.getGroupById(name)
                if group is not None:
                    title = group.getProperty('title') or name
            result.append(dict(name=name, title=title, url=url))
        self.participants = result


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IProjectRoomInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IProjectRoomInfo)
