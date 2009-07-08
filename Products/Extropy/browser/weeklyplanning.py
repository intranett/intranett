from itertools import chain, groupby, ifilterfalse
from operator import attrgetter

from zope.component import getMultiAdapter
from zope.app.publisher.browser.menu import getMenu

from AccessControl import getSecurityManager, Unauthorized
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import monthname_msgid_abbr, utranslate
from Products.CMFPlone.i18nl10n import weekdayname_msgid
from Products.Five import BrowserView

from Products.Extropy.config import OPEN_STATES, TOOLNAME
from timereports import TimeReportQuery

class WeeklyPlanning(BrowserView):
    def __init__(self, context, request):
        super(WeeklyPlanning, self).__init__(context, request)

        start = self.request.get('startdate', None)
        start = start and DateTime(start) or DateTime()
        self.start = start.earliestTime() - (start.dow() - 1) % 7 # Find monday
        self.end = self.start + 7 # next monday 00:00
        self.now = DateTime()

        self.tool = getToolByName(context, TOOLNAME)
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
        month = utranslate('plone', month, context=self.context, default=month)
        return u'%s %02i' % (month, date.day())

    def weekdayname(self, date):
        """Return (localized) weekday name for a date"""
        weekday = weekdayname_msgid(date.dow())
        return utranslate('plone', weekday, context=self.context,
                          default=weekday)

    def taskDetails(self, tasks):
        def jsescape(text):
            return text.replace('\\', '\\\\').replace("'", "\\'")
        for task in tasks:
            progressbar = self.barview(
                task.getWorkedHours, task.getRemainingTime, task.getURL(),
                id='bar-' + task.UID)
            overdue = task.review_state in OPEN_STATES and task.end < self.now
            duedate = ''
            if task.end:
                duedate = self.weekdayname(task.end)
                if task.end < self.start or task.end > self.end:
                    duedate += ' %s' % self.shortDate(task.end)

            yield dict(
                info=task,
                priority=self.tool.getPriorityDescription(task.getPriority),
                overdue=overdue,
                progressbar=progressbar,
                duedate=duedate,
                escaped=dict(
                    project=jsescape(task.getProjectTitle),
                    deliverable=jsescape(task.getPhaseTitle),
                    title=jsescape(task.pretty_title_or_id())
                )
            )

    @property
    def personal_plan(self):
        for i in range(7):
            date = self.start + i
            tasks = self.tool.searchResults(
                getResponsiblePerson=self.user,
                portal_type='ExtropyTask',
                end=dict(query=(date, date.latestTime()), range='min:max'))
            if tasks:
                tasksum = sum(task.getEstimatedDuration for task in tasks)
                yield dict(
                    date=date,
                    weekday=self.weekdayname(date),
                    sum=tasksum,
                    tasks=self.taskDetails(tasks),
                )

    @property
    def overdue(self):
        tasks = self.tool.searchResults(
            portal_type='ExtropyTask',
            end=dict(query=self.start, range='max'),
            review_state=('active', 'assigned'),
            REQUEST=self.request)
        return self.taskDetails(tasks)

    @property
    def unassigned(self):
        tasks = self.tool.searchResults(
            portal_type='ExtropyTask',
            review_state='unassigned',
            REQUEST=self.request)
        return self.taskDetails(tasks)

    @property
    def future(self):
        nodate = ifilterfalse(attrgetter('end'), self.tool.searchResults(
            portal_type='ExtropyTask',
            review_state=('active', 'assigned'),
            REQUEST=self.request))
        tasks = self.tool.searchResults(
            portal_type='ExtropyTask',
            end=dict(query=self.end - 2, range='min'), # from saturday onwards
            review_state=('active', 'assigned'),
            REQUEST=self.request)
        return self.taskDetails(chain(nodate, tasks))

    @property
    def planned(self):
        mtool = getToolByName(self.context, 'portal_membership')
        people = mtool.listMemberIds()
        def earliestEnd(task):
            end = task.end.earliestTime()
            # Ensure a clean date in the server timezone
            return DateTime(end.Date())

        for person in people:
            tasks = self.tool.searchResults(
                portal_type='ExtropyTask',
                getResponsiblePerson=person,
                end=dict(query=(self.start, self.end - 2), range='min:max'),
                sort_on='end')

            # Convert to a date > details dictionary
            by_date = dict((k, self.taskDetails(list(v)))
                           for (k, v) in groupby(tasks, earliestEnd))
            yield dict(user=person,
                       tasks_for_day=(by_date.get(self.start + i, ())
                                      for i in range(5))
                       )

    def assignTask(self, uid, responsible=None, date=None):
        tasks = self.tool.searchResults(UID=uid)
        if not tasks:
            return
        task = tasks[0].getObject()
        task.setResponsiblePerson(responsible)
        task.setEndDate(date)
        task.reindexObject(('getResponsiblePerson', 'end'))

class WeekReport(WeeklyPlanning, TimeReportQuery):
    def __init__(self, context, request):
        super(WeekReport, self).__init__(context, request)
        self.ettool = getToolByName(self.context, 'extropy_timetracker_tool')

    def _query(self):
        # narrow down TimeReportQuery to one user
        self.request['Creator'] = self.user
        super(WeekReport, self)._query()
