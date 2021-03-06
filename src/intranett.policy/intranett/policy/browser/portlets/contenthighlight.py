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

    portletTitle = schema.TextLine(title=_(u"Portlet title"))

    item = schema.Choice(title=_(u"Item"),
        description=_(u"You can select the item to be highlighted by searching on its title."),
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
        return self.item() is not None

    @property
    def portletTitle(self):
        return self.data.portletTitle

    @memoize
    def item(self):
        ct = getToolByName(self.context, 'portal_catalog')
        results = ct.searchResults(UID=self.data.item)
        if results:
            return results[0]
        return None


class AddForm(z3cbase.AddForm):

    fields = field.Fields(IContentHighlight)
    fields['item'].widgetFactory = AutocompleteFieldWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cbase.EditForm):
    fields = field.Fields(IContentHighlight)
    fields['item'].widgetFactory = AutocompleteFieldWidget
