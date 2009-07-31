from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from Products.Extropy.browser.timereports import TimeReportQuery
from Products.Extropy.config import INVOICE_RELATIONSHIP


class InvoicingError(ValueError):
    """Error invoicing hour objects"""


class InvoiceHours(BrowserView, TimeReportQuery):
    """Hours associated with an invoice"""

    def __init__(self, context, request):
        super(InvoiceHours, self).__init__(context, request)
        self.ettool = getToolByName(self.context, 'extropy_timetracker_tool')

    def _query(self):
        uids = [r.sourceUID
                for r in self.context.getBackReferenceImpl(INVOICE_RELATIONSHIP)]

        self._hours = self.ettool.getHours(UID=uids)
        self._sum = self.ettool.countHours(self._hours)

    def email_hours_report(self):
        timefmt = '%h.%d %H:%M';
        result = []
        for data in self.hours_by_date:
            if data['hours']:
                result.append('-' * 20)
                result.append(data['date'].strftime('%A %d %b'))
                for hour in data['hours']:
                    result.append('%s to %s (%s hours)   : %s' % (
                        hour.start.TimeMinutes(), hour.end.TimeMinutes(),
                        hour.workedHours, hour.Title.ljust(25)))
                result.append("total: %s hours\n" % data['sum'])
        result.append('-' * 60)
        result.append('Total hours: %s' % self.sum)
        result.append('=' * 60)
        return '\n'.join(result)
