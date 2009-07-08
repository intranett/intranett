#
# ExtropyTrackingTestCase Skeleton
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from DateTime import DateTime



class Dummyhours:
    """fake worked hours"""
    def __init__(self, hours):
        self.workedHours = hours



class TestTool(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.tool = self.portal.extropy_timetracker_tool

    def testTimeTrackerToolExists(self):
        self.failUnless('extropy_timetracker_tool' in self.portal.objectIds())

    def testConvertingHours(self):
        self.assertEqual(self.tool.convertHours(48), 2)
        self.assertEqual(self.tool.convertHours(24), 1)
        self.assertEqual(self.tool.convertHours(12), 0.5)

    def testGetDefaultStart(self):
        self.failIfEqual(self.tool.getLastRegisteredTime(), self.tool.getDefaultStartTime())

    def testGetDefaultStart2(self):
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=1)
        h = self.folder.hourglass.objectValues()[0]
        self.assertEqual(h.end(), self.tool.getDefaultStartTime())
        self.assertEqual(h.start() + self.tool.convertHours(1), self.tool.getDefaultStartTime())

    def testaddTimeTrackingHours(self):
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=1)
        self.failUnless('hourglass' in self.folder.objectIds())
        self.failUnless(len(self.folder.hourglass.objectIds())==1)
        self.assertEqual(self.folder.hourglass.objectValues()[0].Title(),  'testing')
        self.assertEqual(self.folder.hourglass.objectValues()[0].workedHours(),1)

    def testaddTimeTrackingHours2(self):
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=1)
        hour = self.folder.hourglass.objectValues()[0]
        #print 30*"*"
        #print hour.start()
        #print hour.end()
        #print hour.workedHours()
        self.assertEqual(hour.end(),hour.start()+ self.tool.convertHours(1))
        self.assertEqual(hour.workedHours(), 1)

    def testGettingHours(self):
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=5)
        self.assertEqual(len(self.tool.getHours(node=self.folder)),1)
        self.assertEqual(self.tool.getHours(node=self.folder)[0].workedHours,5)


    def testCountHoursBasic(self):
        class Foo:
            """fake worked hours"""
            def __init__(self, hours):
                self.workedHours = hours

        f = Foo(5)
        self.assertEqual(self.tool.countHours([f]),5)

    def testCountingHours(self):
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=5)
        newhours = self.tool.getHours(node=self.folder)[0]
        self.assertEqual(newhours.getObject().workedHours(), 5)
        self.assertEqual(newhours.workedHours, 5)
        self.assertEqual(self.tool.countIntervalHours(node=self.folder),5)

    def testCountingHours2(self):
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=5)
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=3)
        self.assertEqual(self.tool.countIntervalHours(node=self.folder),8)

    def testCountingHours3(self):
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=5)
        h = self.tool.getHours(node=self.folder)
        self.assertEqual(len(h),1)
        self.assertEqual(h[0].workedHours, 5)
        self.assertEqual(h[0].getObject().workedHours(), 5)
        self.assertEqual(self.tool.countHours(h), 5)

    def testMinMaxQueries(self):
        ttt = self.portal.extropy_timetracker_tool
        self.folder.invokeFactory('Folder', 'extropy')
        folder = self.folder.extropy
        _createObjectByType('ExtropyHourGlass',folder, 'hourglass')
        folder.hourglass.invokeFactory('ExtropyHours','test1', startDate='2001/01/01', endDate='2001/01/02')
        folder.hourglass.invokeFactory('ExtropyHours','test2', startDate='2002/01/01', endDate='2002/01/02')
        folder.hourglass.invokeFactory('ExtropyHours','test3', startDate='2008/02/01', endDate='2008/02/02')

        ttt = getToolByName(self.portal, 'extropy_timetracker_tool')

        self.assertEqual(len(ttt.getHours(node=self.folder)),3)
        self.assertEqual(len(ttt.getHours(node=self.folder, start='2003/01/01',end='2003/01/02' )),0)
        self.assertEqual(len(ttt.getHours(node=self.folder, start='2003/01/01')),1)
        self.assertEqual(len(ttt.getHours(node=self.folder, end='2003/01/01')),2)

    def testFillGaps(self):
        date = DateTime().Date()
        start = DateTime('%s 08:00' % date)
        end = DateTime('%s 17:00' % date)
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=5, start=DateTime('%s 09:00' % date))
        self.tool.addTimeTrackingHours(self.folder, 'testing2', hours=1, start=DateTime('%s 15:00' % date))
        hours = self.tool.getHours(node=self.folder)
        res = self.tool.fillGaps(hours)
        self.failUnlessEqual(len(res), 3) # Supposed to fill the hour between 14 and 15
        res = self.tool.fillGaps(hours, start=DateTime('%s 08:00' % date))
        self.failUnlessEqual(len(res), 4) # Fill leading gap
        res = self.tool.fillGaps(hours, end=DateTime('%s 18:00' % date))
        self.failUnlessEqual(len(res), 5) # Supposed to fill two hours between 16 and 18

    def testFillGapsNoGap(self):
        date = DateTime().Date()
        self.tool.addTimeTrackingHours(self.folder, 'testing', hours=1, start=DateTime('%s 09:00' % date))
        self.tool.addTimeTrackingHours(self.folder, 'testing2', hours=1, start=DateTime('%s 10:00' % date))
        hours = self.tool.getHours(node=self.folder)
        res = self.tool.fillGaps(hours)
        self.failUnlessEqual(len(res), 2)

    def testFillGapsWithNoHours(self):
        date = DateTime().Date()
        start = DateTime('%s 08:00' % date)
        end = DateTime('%s 17:00' % date)
        hours = self.tool.getHours(node=self.folder)
        res = self.tool.fillGaps(hours, start=start, end=end)
        self.assertEqual(len(res),9)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTool))
    return suite

if __name__ == '__main__':
    framework()
