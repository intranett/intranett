#
# ExtropyTrackingTestCase Skeleton
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from DateTime import DateTime
import re
from Products.CMFPlone.utils import _createObjectByType, getToolByName

from zope.component import getMultiAdapter
from zope.interface import Interface

from Products.Extropy.browser.timereports import InvoicingError

class TestTimeReportViews(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        hour = 1.0/24.0
        now = DateTime()
        _createObjectByType('ExtropyHours', self.folder, 'hours1',
                            title='Hour entry 1',
                            budgetCategory='Billable',
                            startDate=now - (hour * 2),
                            endDate=now
                            )
        _createObjectByType('ExtropyHours', self.folder, 'hours2',
                            title='Hour entry 2',
                            budgetCategory='Administration',
                            startDate=now - (hour * 4),
                            endDate=now - (hour * 2)
                            )

    def getView(self, name):
        return getMultiAdapter((self.folder, self.app.REQUEST), Interface,
                               name).__of__(self.folder)

    def testTimeReportView(self):
        html = self.getView('timereport')()
        self.assertTrue('Hour entry 1' in html)
        self.assertTrue('Hour entry 2' in html)
        self.assertTrue('Billable' in html)
        self.assertTrue('Administration' in html)
        self.assertTrue('2.0' in html)
        self.assertTrue('4.0' in html)

    def testFinanceAccess(self):
        view = self.getView('timereport')
        self.assertFalse(view.finance_access)

        self.setRoles(('Finance-manager',))
        self.assertTrue(view.finance_access)

    def testSelectedHours(self):
        view = self.getView('timereport')
        self.assertEqual(list(view.selected_hours), [])

        self.app.REQUEST.set('hours',
                             ['/'.join(self.folder.hours1.getPhysicalPath())])
        view = self.getView('timereport')
        self.assertEqual(list(view.selected_hours), [self.folder.hours1])

    def testSelectedNonBillable(self):
        self.app.REQUEST.set('hours',
                             ['/'.join(self.folder.hours2.getPhysicalPath())])
        view = self.getView('timereport')
        self.assertRaises(InvoicingError, list, view.selected_hours)

    def testSelectedInvoiced(self):
        wf_tool = getToolByName(self.folder, 'portal_workflow')
        wf_tool.doActionFor(self.folder.hours1, 'invoice')

        self.app.REQUEST.set('hours',
                             ['/'.join(self.folder.hours1.getPhysicalPath())])
        view = self.getView('timereport')
        self.assertRaises(InvoicingError, list, view.selected_hours)

    def testEmailHoursReport(self):
        text = self.getView('email_hours_report')()
        self.assertTrue('Hour entry 1' in text)
        self.assertTrue('Hour entry 2' in text)
        self.assertTrue('2.0' in text)
        self.assertTrue('4.0' in text)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTimeReportViews))
    return suite

if __name__ == '__main__':
    framework()
