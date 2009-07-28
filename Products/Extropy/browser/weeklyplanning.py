from zope.component import getMultiAdapter
from zope.app.publisher.browser.menu import getMenu

from AccessControl import getSecurityManager, Unauthorized
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import monthname_msgid_abbr, utranslate
from Products.CMFPlone.i18nl10n import weekdayname_msgid
from Products.Five import BrowserView

from Products.Extropy.config import TOOLNAME
from timereports import TimeReportQuery


class WeekReport(BrowserView, TimeReportQuery):

    def __init__(self, context, request):
        super(WeekReport, self).__init__(context, request)

        start = self.request.get('startdate', None)
        start = start and DateTime(start) or DateTime()
        self.start = start.earliestTime() - (start.dow() - 1) % 7 # Find monday
        self.end = self.start + 7 # next monday 00:00
        self.now = DateTime()

        self.tool = getToolByName(context, TOOLNAME)
        self.ettool = getToolByName(self.context, 'extropy_timetracker_tool')
        self.barview = getMultiAdapter((self.context, self.request),
                                       name=u'smallprogressbar')

    @property
    def next(self):
        return self.start + 7

    @property
    def prev(self):
        return self.start - 7

    @property
    def user(self):
        user = getSecurityManager().getUser().getUserName()
        if user == 'Anonymous User':
            raise Unauthorized('Must be logged in to use this view')
        return self.request.get('user', user)

    @property
    def menu(self):
        for mitem in getMenu('weeklyplan', self.context, self.request):
            if not mitem['selected']:
                # workaround for Zope bug #2288, don't include @@ in action
                mitem['action'] = mitem['action'].replace('@@', '')
                yield mitem

    @property
    def weekdays(self):
        for i in range(5):
            date = self.start + i
            yield '%s %s' % (self.weekdayname(date), self.shortDate(date))

    @property
    def responsibles(self):
        return filter(None, self.tool.uniqueValuesFor('getResponsiblePerson'))

    @property
    def projects(self):
        return self.tool.searchResults(portal_type='ExtropyProject',
                                       review_state='active')

    def shortDate(self, date):
        """Format date in "Feb 06" style"""
        month = monthname_msgid_abbr(date.month())
        month = utranslate('plonelocales', month, context=self.request, default=month)
        return u'%s %02i' % (month, date.day())

    def weekdayname(self, date):
        """Return (localized) weekday name for a date"""
        weekday = weekdayname_msgid(date.dow())
        return utranslate('plonelocales', weekday, context=self.request,
                          default=weekday)

    def _query(self):
        # narrow down TimeReportQuery to one user
        self.request['Creator'] = self.user
        super(WeekReport, self)._query()
