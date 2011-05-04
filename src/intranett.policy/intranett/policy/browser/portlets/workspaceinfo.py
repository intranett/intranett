from DateTime import DateTime
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
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
        return hasattr(self.context, 'getWorkspacestate')

    @property
    def portletTitle(self):
        return _("Workspace Info")


class AddForm(base.AddForm):

    form_fields = form.Fields(IWorkspaceInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = form.Fields(IWorkspaceInfo)
