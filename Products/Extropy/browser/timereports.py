from itertools import groupby
from operator import attrgetter

from zope.app.publisher.browser.menu import getMenu

from AccessControl import getSecurityManager
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import transaction_note
from Products.Five import BrowserView
from ZTUtils import make_query

from Products.Extropy.config import INVOICE_RELATIONSHIP
from Products.Extropy.permissions import MANAGE_FINANCES

class TimeReportQuery(object):
    """Mixin class for timereport queries"""
    _hours = None
    _sum = None

    def _query(self):
        self._hours = self.ettool.getHours(self.context, start=self.start,
                                           end=self.end, REQUEST=self.request)
        self._sum = self.ettool.countHours(self._hours)

    def _clearQuery(self):
        self._hours = self._sum = None

    @property
    def hours(self):
        if self._hours is None:
            self._query()
        return self._hours

    @property
    def sum(self):
        if self._sum is None:
            self._query()
        return self._sum

    @property
    def people(self):
        return self.ettool.uniqueValuesFor('Creator')

    @property
    def categories(self):
        return self.ettool.uniqueValuesFor('getBudgetCategory')

    @property
    def hours_by_category(self):
        hours = list(self.hours)
        category = attrgetter('getBudgetCategory')
        hours.sort(key=category)
        for category, hours in groupby(hours, category):
            yield dict(category=category,
                       sum=self.ettool.countHours(hours))

    @property
    def hours_by_date(self):
        def earliestStart(hour):
            start = hour.start.earliestTime()
            # Ensure a clean date in the server timezone
            return DateTime(start.Date())
        hours = list(self.hours)
        hours.sort(key=earliestStart)
        by_date = dict((k, tuple(v))
                       for (k, v) in groupby(hours, earliestStart))
        for date, hours in groupby(hours, earliestStart):
            hours = tuple(hours)
            yield dict(date=date, hours=hours,
                       sum=self.ettool.countHours(hours))

    @property
    def hours_by_project(self):
        hours = list(self.hours)
        project = attrgetter('getProjectTitle')
        hours.sort(key=project)
        for project, hours in groupby(hours, project):
            hours = tuple(hours)
            sum = self.ettool.countHours(hours)
            yield dict(project=project, category=hours[0].getBudgetCategory,
                       sum=sum)


class InvoicingError(ValueError):
    """Error invoicing hour objects"""

class TimeReports(BrowserView, TimeReportQuery):
    def __init__(self, context, request):
        super(TimeReports, self).__init__(context, request)

        self.ettool = getToolByName(self.context, 'extropy_timetracker_tool')

        start = self.request.get('startdate', None)
        start = start and DateTime(start) or (DateTime('2000-01-01'))
        self.start = start.earliestTime()

        end = self.request.get('enddate', None)
        end = end and DateTime(end) or DateTime()
        self.end = end.latestTime()

        self.query_string = make_query(*(
            {key: self.request[key]}
            for key in ('Creator', 'getBudgetCategory', 'startdate', 'enddate')
            if key in self.request))
        self.query_string = self.query_string and '?' + self.query_string

    def __call__(self, *args, **kw):
        if 'mark_invoiced' in self.request:
            self.mark_invoiced()
        if 'create_invoice' in self.request:
            invoice = self.create_invoice()
            return self.request.response.redirect(invoice.absolute_url())
        return super(TimeReports, self).__call__(*args, **kw)

    @property
    def menu(self):
        for mitem in getMenu('timereport', self.context, self.request):
            if not mitem['selected']:
                # workaround for Zope bug #2288, don't include @@ in action
                mitem['action'] = mitem['action'].replace('@@', '')
                yield mitem

    @property
    def finance_access(self):
        """Does the current user have permission to manage finances"""
        # This needs to be a property, because PlonePAS cannot determine the
        # user yet at traversal time, which is when the view gets instantiated
        user = getSecurityManager().getUser()
        return user.has_permission(MANAGE_FINANCES, self.context)

    @property
    def can_construct_invoices(self):
        """Can invoices be constructed for the current context"""
        types_tool = getToolByName(self.context, 'portal_types')
        context_info = types_tool.getTypeInfo(self.context)
        invoice_info = types_tool.getTypeInfo('Invoice')
        if context_info and not context_info.allowType('Invoice'):
            return False
        return invoice_info.isConstructionAllowed(self.context)

    @property
    def invoice_states(self):
        return self.ettool.uniqueValuesFor('review_state')

    @property
    def selected_hours(self):
        selected = self.request.get('hours', ())
        for hour in self.hours:
            if hour.getPath() in selected:
                if hour.getBudgetCategory != 'Billable':
                    raise InvoicingError, 'Selected hour is not billable'
                if hour.review_state != 'entered':
                    raise InvoicingError, 'Selected hour is already invoiced'
                yield hour.getObject()

    def can_invoice(self, hour):
        """Determine if the given hour report can be invoiced"""
        return (hour.getBudgetCategory == 'Billable' and
                hour.review_state == 'entered')

    def setMessage(self, message):
        tool = getToolByName(self.context, 'plone_utils')
        tool.addPortalMessage(message)
        transaction_note(message)

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
        result.append('Total hours between %s and %s : %s' % (
            self.start.Date(), self.end.Date(), self.sum,))
        result.append('=' * 60)
        return '\n'.join(result)

    def mark_invoiced(self):
        """Mark the selected hours as invoiced"""
        wf_tool = getToolByName(self.context, 'portal_workflow')
        for hour in self.selected_hours:
            wf_tool.doActionFor(hour, 'invoice')
        self._clearQuery()
        self.setMessage('Marked hours as invoiced.')

    def create_invoice(self):
        """Create an invoice from the selected hours"""
        id = self.context.aq_inner.generateUniqueId('Invoice')
        new_id = self.context.aq_inner.invokeFactory(id=id, type_name='Invoice')
        invoice = getattr(self.context.aq_inner, new_id or id)

        for hour in self.selected_hours:
            hour.deleteReferences(INVOICE_RELATIONSHIP)
            hour.addReference(invoice, INVOICE_RELATIONSHIP)

        self.setMessage('Created invoice from marked hours.')
        self.mark_invoiced()

        return invoice
