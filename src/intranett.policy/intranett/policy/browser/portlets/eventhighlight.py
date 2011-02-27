from Acquisition import aq_inner
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


class IEventHighlight(IPortletDataProvider):
    """A portlet for displaying recent news items on the front page.
    """

    portletTitle = schema.TextLine(title=_(u"Portlet title"), description=u"")


class Assignment(base.Assignment):

    implements(IEventHighlight)

    def __init__(self, portletTitle=""):
        self.portletTitle = portletTitle

    title = _("Event Highlight")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('eventhighlight.pt')

    @property
    def available(self):
        return self.item is not None

    @property
    def portletTitle(self):
        return self.data.portletTitle

    @memoize
    def upcomingEvent(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        event = catalog(portal_type='Event',
                        review_state='published',
                        end={'query': DateTime(),
                             'range': 'min'},
                        sort_on='start',
                        sort_limit=1)[:1]
        event = event and event[0] or None
        return event

    @property
    def item(self):
        return self.upcomingEvent()


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IEventHighlight)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IEventHighlight)
