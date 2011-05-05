from plone.app.portlets.portlets import base
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.portlets.interfaces import IPortletDataProvider
from plone.z3cform.layout import FormWrapper
from plone.principalsource.source import UsersVocabularyFactory
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button, field, form
from zope.formlib import form as formlibform
from zope.interface import Interface
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
        self.title = self.context.Title()
        members = self.context.members
        members = map(self.context.portal_membership.getMemberById, members)
        self.members = tuple(member.getProperty("fullname") or member.getId() for member in members)
        self.membersform = WSMemberFormWrapper(self.context, self.request)
        self.membersform.update()


class AddForm(base.AddForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):

    form_fields = formlibform.Fields(IWorkspaceInfo)


class IWSMemberForm(Interface):

    username = zope.schema.Choice(
        title=_(u"Add user"),
        source=UsersVocabularyFactory)


class WSMemberForm(form.EditForm):
    """An edit form for the workspace.
    """
    fields = field.Fields(IWSMemberForm)
    fields['username'].widgetFactory = AutocompleteFieldWidget

    ignoreContext = True
    label = _(u"Add workspace member")

    def applyChanges(self, data):
        ws = self.context.getWorkspace()
        members = ws.members
        if data['username'] not in members:
            members += (data['username'],)
            ws.members = members
            return True
        else:
            return False

    def nextURL(self):
        ws = self.context.getWorkspace()
        return ws.absolute_url() + '/@@members-edit'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='apply')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = "Changes saved"
        else:
            self.status = "No changes"

        self.request.response.redirect(self.nextURL())
        return ''

    #@button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"), name='cancel_add')
    #def handleCancel(self, action):
    #    self.request.response.redirect(self.nextURL())
    #    return ''


class WSMemberFormWrapper(FormWrapper):

    form = WSMemberForm
    index = ViewPageTemplateFile('members-edit-form.pt')

