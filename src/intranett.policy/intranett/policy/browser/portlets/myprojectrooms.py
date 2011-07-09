from AccessControl import getSecurityManager
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form as formlibform
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _


class IMyProjectRooms(IPortletDataProvider):
    pass


class Assignment(base.Assignment):

    implements(IMyProjectRooms)

    title = _("My project rooms")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('myprojectrooms.pt')
    portletTitle = _("My project rooms")
    available = True

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        user_id = getSecurityManager().getUser().getId()
        query = dict(
            portal_type="ProjectRoom",
            participants=(user_id, ),
            sort_on='sortable_title'
        )
        self.projectrooms = ({'title': x.Title, 'url': x.getURL()}
            for x in catalog(query))


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IMyProjectRooms)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IMyProjectRooms)
