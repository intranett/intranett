from plone.app.portlets.portlets import base
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.portlets.interfaces import IPortletDataProvider
from plone.principalsource.source import UsersVocabularyFactory
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button, field, form
from zope.formlib import form as formlibform
from zope.interface import implements
import zope.schema

from intranett.policy import IntranettMessageFactory as _


class IWorkspaceInfo(IPortletDataProvider):
    """Provides information such as members and visibility of a workspace"""


class Assignment(base.Assignment):

    implements(IWorkspaceInfo)

    title = _("Workspace Info")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('workspaceinfo.pt')
    username = zope.schema.Choice(title=_(u"User"),
        description=_(u"Select the user to be added"),
        source=UsersVocabularyFactory)

    @property
    def available(self):
        return hasattr(self.context, 'getWorkspaceState')

    @property
    def portletTitle(self):
        return _("Workspace Info")
    
    def update(self):
        if not self.available:
            return
        wf = getToolByName(self.context, 'portal_workflow')
        self.state = wf.getInfoFor(self.context, "workspace_visibility")
        self.title = self.context.getWorkspace().Title()
        members = self.context.members
        members = map(self.context.portal_membership.getMemberById, members)
        self.members = tuple(member.getProperty("fullname") for member in members)
        import pdb; pdb.set_trace( )
        NotImplemented



class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)

