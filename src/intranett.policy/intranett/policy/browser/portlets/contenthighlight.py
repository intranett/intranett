from plone.app.portlets.portlets import base as formlibbase
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope import schema
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _
from intranett.policy.browser.portlets import z3cbase
from intranett.policy.browser.sources import DocumentSourceBinder


class IContentHighlight(IPortletDataProvider):
    """A portlet for displaying a selected content item on the front page.
    """

    portletTitle = schema.TextLine(
        title = _(u"Portlet title"),
        description = u"")

    item = schema.Choice(title=_(u"Item"),
                         source=DocumentSourceBinder(),
                         required=True)


class Assignment(formlibbase.Assignment):

    implements(IContentHighlight)

    def __init__(self, portletTitle="", item=None):
        self.portletTitle = portletTitle
        self.item = item

    title = _("Content Highlight")


class Renderer(formlibbase.Renderer):

    render = ViewPageTemplateFile('contenthighlight.pt')

    @property
    def available(self):
        return self.item

    @property
    def portletTitle(self):
        return self.data.portletTitle

    @property
    @memoize
    def item(self):
        ct = getToolByName(self.context, 'portal_catalog')
        results = ct.searchResults(UID=self.data.item)
        if results:
            return results[0]


class AddForm(z3cbase.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    fields = field.Fields(IContentHighlight)
    fields['item'].widgetFactory = AutocompleteFieldWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cbase.EditForm):
    fields = field.Fields(IContentHighlight)
    fields['item'].widgetFactory = AutocompleteFieldWidget
