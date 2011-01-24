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

    @property
    def available(self):
        return not self.portal_state.anonymous()

    def totals(self):
        """Gets the content."""
        etool = getToolByName(self.context, TIMETOOLNAME)
        membership = getToolByName(self.context, 'portal_membership')
        portal = self.portal_state.portal()
        now = DateTime()
        startOfWeek = now.earliestTime() - (now.dow()-1)%7
        endOfWeek = (startOfWeek + 6).latestTime()

        brains = list(etool.getHours(node=portal, start=startOfWeek,
                                      end=endOfWeek, REQUEST=None))
        results = []
        creator = attrgetter('Creator')
        brains.sort(key=creator)
        for person, hours in groupby(brains, creator):
            member = membership.getMemberInfo(person)
            fullname = member.get('fullname', person)
            results.append(((fullname, person), etool.countHours(hours)))
        results.sort()
        return results


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
