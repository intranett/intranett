from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFPlone.utils import _createObjectByType

from DateTime import DateTime
from Products.Extropy.browser.managementreports import WeeklyReport


class Dummyhours:
    """fake worked hours"""
    def __init__(self, hours):
        self.workedHours = hours

class TestReportViews(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.tool = self.portal.extropy_timetracker_tool
        self.request = self.app.REQUEST

    def testInstantiateView(self):
        view = WeeklyReport(self.portal, self.request)

    def testGettingHours(self):
        view = WeeklyReport(self.portal, self.request)
        self.folder.invokeFactory('Folder', 'extropy')
        folder = self.folder.extropy
        _createObjectByType('ExtropyHourGlass',folder, 'hourglass')
        folder.hourglass.invokeFactory('ExtropyHours','test1', startDate=DateTime()-3.1, endDate=DateTime()-3)
        folder.hourglass.invokeFactory('ExtropyHours','test2', startDate=DateTime()-3.1, endDate=DateTime()-3)
        folder.hourglass.invokeFactory('ExtropyHours','test3', startDate=DateTime()-3.2, endDate=DateTime()-3)
        self.assertEqual(len(view.getHours()),3)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestReportViews))
    return suite
