from itertools import groupby

from zope.interface import Interface
from zope.publisher.browser import BrowserView

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName


def earliestStart(hour):
    start = hour.start.earliestTime()
    # Ensure a clean date in the server timezone
    return DateTime(start.Date())


def countHours(hours):
    return sum(h.workedHours for h in hours)


class IInvoiceHours(Interface):

    def getNumber():
        """Get the number"""

    def getHours():
        """Get the hours"""


class InvoiceHours(BrowserView):
    """invoice hour report"""

    def getNumber(self):
        return self.request.form.get('number', None)

    def _queryHours(self, number):
        ettool = getToolByName(self.context, 'extropy_timetracker_tool')
        query = dict()
        query['getInvoiceNumber'] = number
        query['portal_type'] = 'ExtropyHours'
        query['sort_on'] = 'start'
        brains = list(ettool.searchResults(query))
        brains.sort(key=earliestStart)
        return brains

    def getHours(self):
        number = self.getNumber()
        if not number:
            return []

        brains = self._queryHours(number)
        hours_by_date = []
        for date, hours in groupby(brains, earliestStart):
            hours = tuple(hours)
            hours_by_date.append(dict(date=date, hours=hours,
                                 sum=countHours(hours)))

        result = []
        for data in hours_by_date:
            if data['hours']:
                result.append(data['date'].strftime('%A %d %b'))
                for hour in data['hours']:
                    result.append('%s to %s (%s hours) : %s' % (
                        hour.start.TimeMinutes(), hour.end.TimeMinutes(),
                        hour.workedHours, hour.Title.ljust(25)))
                result.append("total: %s hours%s" % (data['sum'], '<br />'))

        if not result:
            return ''
        result.append('Total hours: %s' % countHours(brains))
        return '<br />'.join(result)
