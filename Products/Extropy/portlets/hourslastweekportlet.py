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


class IHourslastweekPortlet(IPortletDataProvider):
    """A portlet which renders work hours.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IHourslastweekPortlet)

    def __init__(self):
        pass
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return "hourslastweek"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('hourslastweekportlet.pt')

    @property
    def available(self):
        return True


    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()

    def myhours(self):
        """Gets the content."""
        etool = getToolByName(self, TIMETOOLNAME)
        portal = self.portal
        user = getSecurityManager().getUser().getUserName()
        now = DateTime()
        start = now.earliestTime() - 6
        end = now.latestTime()
        hours = list(etool.getHours(node=portal, start=start, end=end,
                                    REQUEST=None, Creator=user))

        def earliestStart(hour):
            start = hour.start.earliestTime()
            # Ensure a clean date in the server timezone
            return DateTime(start.Date())

        hours.sort(key=earliestStart)
        by_date = dict((k, tuple(v))
                       for (k, v) in groupby(hours, earliestStart))
        results = []
        for i in range(7):
            date = start + i
            hours = by_date.get(date, ())
            results.append(dict(date=date,
                                sum=etool.countHours(hours)))
        return results


    def reportlink(self):
        "link to the more detailed view"
        return "%s/weeklyplan_report" %(self.portal_url,)
        
        
class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()

