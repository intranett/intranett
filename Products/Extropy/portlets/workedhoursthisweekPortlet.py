from itertools import groupby
from operator import attrgetter

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.interface import implements

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.Extropy.config import TIMETOOLNAME


class IWorkedHoursPortlet(IPortletDataProvider):
    """A portlet which renders work hours.
    """


class Assignment(base.Assignment):
    """Portlet assignment.
    """

    implements(IWorkedHoursPortlet)
    title = "Worked hours"


class Renderer(base.Renderer):
    """A class for showing all the worked hours this week."""

    render = ViewPageTemplateFile('portlet_workedhours_contents.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        self.portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal_url = self.portal_state.portal_url()
        self.portal = self.portal_state.portal()

    @property
    def available(self):
        return not self.portal_state.anonymous()

    def totals(self):
        """Gets the content."""
        etool = getToolByName(self, TIMETOOLNAME)
        portal = self.portal
        now = DateTime()
        startOfWeek = now.earliestTime() - (now.dow()-1)%7
        endOfWeek = (startOfWeek + 6).latestTime()

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
