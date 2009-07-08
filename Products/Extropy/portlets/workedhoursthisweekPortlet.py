from itertools import groupby
from operator import attrgetter
from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Products.Extropy.config import *
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from DateTime import DateTime
from itertools import groupby

from plone.i18n.normalizer.interfaces import IIDNormalizer

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlet.static import PloneMessageFactory as _
from DateTime import DateTime

class IWorkedHoursPortlet(IPortletDataProvider):
    """A portlet which renders work hours.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IWorkedHoursPortlet)

    def __init__(self):
        pass
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return "workedhours"


class Renderer(base.Renderer):
    """A class for showing all the worked hours this week."""


    render = ViewPageTemplateFile('portlet_workedhours_contents.pt')

    @property
    def available(self):
        return True


    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()



    def totals(self):
        """Gets the content."""
        etool = getToolByName(self, TIMETOOLNAME)
        portal = self.portal
        user = getSecurityManager().getUser().getUserName()
        now = DateTime()
        startOfWeek = now.earliestTime() - (now.dow()-1)%7
        endOfWeek = (startOfWeek + 6 ).latestTime()

        results = list(etool.getHours(node=portal, start=startOfWeek,
                                      end=endOfWeek, REQUEST=None))
        person = attrgetter('Creator')
        results.sort(key=person)

        totals = {}
        for person, hours in groupby(results, person):
            totals[person] = etool.countHours(hours)
        return totals


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
