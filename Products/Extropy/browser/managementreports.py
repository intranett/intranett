from itertools import groupby
from operator import attrgetter
from zope import interface
from Products import Five
from DateTime import DateTime
from Products.Extropy import config
from Products.CMFCore.utils import getToolByName


class IWeeklyReport(interface.Interface):
    def getParticipants():
        """Get the people involved.
        """

    def start():
        """date to the report starts"""

    def end():
        """date the report ends"""

    def getWorkedHours():
        """get the hours worked in the deinfed timespan"""

    def hoursByDate(hours):
        """split a set of hours by date"""

    def hoursByPerson(hours):
        """split a set of hours by person"""

    def hoursByGroup(hours):
        """hours by budget groups"""

    def hoursByPersonAndGroup():
        """a dict of people with hours by budget category"""


class WeeklyReport(Five.BrowserView):
    """Helper view for task editing
    """

    def __init__(self, context, request):
        Five.BrowserView.__init__(self, context, request)
        self.hours=None

    def getParticipants(self):
        """get the people involved"""
        return ['geir','tesdal']

    def start(self):
        """startdate"""
        return (DateTime()-7).earliestTime()

    def end(self):
        """enddate"""
        return (self.start()+7).latestTime()

    def getHours(self):
        """ hours"""
        return getToolByName(self.context, config.TIMETOOLNAME).getHours(self.context, start=self.start(), end=self.end(), REQUEST=self.request)

    def getHoursByPerson(self):
        """"""
        hours = list(self.getHours())
        person = attrgetter('Creator')
        hours.sort(key=person)
        return dict((k, tuple(v)) for (k, v) in groupby(hours, person))


class IInvoiceReport(interface.Interface):

    def getInvoices():
        """Get the Invoices
        """


class InvoiceReport(Five.BrowserView):
    """invoices report"""

    def getInvoices(self):
        etool = getToolByName(self.context, config.TOOLNAME)
        anchor = etool.getQueryAnchor(self.context)
        pc = getToolByName(self.context, 'portal_catalog',  )
        invoices = pc.searchResults(Type='Invoice', path='/'.join(anchor.getPhysicalPath()))
        return [i.getObject() for i in invoices]

    def sumInvoices(self, invoices):
        if invoices is None or len(invoices)==0 or not invoices:
            return 0
        total = 0
        for i in invoices:
            t = i.getTotal()
            if isinstance(t, int):
                # We sometimes get 0.0 or *error* here
                total += t
        return total

    def splitInvoicesByState(self,invoices):
        d={}
        wftool = getToolByName(self, 'portal_workflow')
        for i in invoices:
            newkey = wftool.getInfoFor(i, 'review_state')
            if d.has_key(newkey):
                if d[newkey].has_key('invoices'):
                    d[newkey]['invoices'].append(i)
            else:
                d[newkey]={'invoices':[i]}
        for k in d.keys():
            d[k]['total']=self.sumInvoices(d[k]['invoices'])
        return d

    def getInvoicesByState(self):
        invoices = self.getInvoices()
        return self.splitInvoicesByState(invoices)

    def getStates(self):
        return self.getInvoicesByState().keys()
