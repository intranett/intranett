#
# ExtropyTrackingTestCase Skeleton
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.Extropy.config import TIMETOOLNAME
from DateTime import DateTime
from Products.CMFPlone.utils import _createObjectByType


class TestExtropyHourSetup(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.timetracktool = getattr(self.portal,TIMETOOLNAME)

    def testAddingHourGlass(self):
        # test that we can add
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass')
        self.failUnless('hourglass' in self.folder.objectIds())

    def testAddingHour(self):
        # test that we can add an hour
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass')
        self.folder.hourglass.invokeFactory('ExtropyHours','test')
        self.failUnless('test' in self.folder.hourglass.objectIds())

    def testCatalogingHours(self):
        # test that hours get cataloged properly in the tool
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass')
        self.folder.hourglass.invokeFactory('ExtropyHours','test')
        self.failUnless(len(self.timetracktool())==1)

    def testCatalogingHoursOnlyInTheTimeTrackTool(self):
        # test that hours get cataloged ONLY in the tool
        l = len( self.portal.portal_catalog() )
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass')
        # HourGlasses dont get cataloged anywhere
        self.folder.hourglass.invokeFactory('ExtropyHours','test')
        #the number of objects in the catalog should not increasae
        self.failIf( len( self.portal.portal_catalog() ) != l )


class TestExtropyHours(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.timetracktool = getattr(self.portal,TIMETOOLNAME)
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass')
        self.hourglass = getattr(self.folder, 'hourglass')
        self.now = DateTime()
        self.h = 1.0/24.0

    def testWorkHours(self):
        self.hourglass.invokeFactory('ExtropyHours','a',startDate=self.now-(self.h*2), endDate=self.now-self.h)
        a = getattr(self.hourglass, 'a')
        self.failUnless(a.workedHours()==1)

    def testCataloging(self):
        self.hourglass.invokeFactory('ExtropyHours','a',startDate=self.now-(self.h*2), endDate=self.now-self.h)
        a = getattr(self.hourglass, 'a')
        self.failUnless(len(self.timetracktool.searchResults())==1)
        self.assertEqual(self.timetracktool.searchResults()[0].getObject(), a)

    def testCataloging2(self):
        self.hourglass.invokeFactory('ExtropyHours','a',startDate=self.now-(self.h*2), endDate=self.now-self.h)
        self.assertEqual(self.timetracktool.searchResults()[0].workedHours, 1)

    def testToolIntervalQuery(self):
        self.hourglass.invokeFactory('ExtropyHours','a',startDate=self.now-(self.h*2), endDate=self.now-self.h)
        self.hourglass.invokeFactory('ExtropyHours','b',startDate=self.now-2, endDate=self.now - (2 + self.h))
        self.assertEqual(len(self.timetracktool.searchResults()),2)
        self.assertEqual(len(self.timetracktool.getHours( start=self.now -1, end=self.now )),1)
        self.assertEqual(len(self.timetracktool.getHours( start=self.now -3, end=self.now ) ),2)
        self.assertEqual(len(self.timetracktool.getHours( start=self.now +1, end=self.now + 2 ) ),0)


    def testToolIntervalCounting(self):
        # add a one-hour tracking
        self.hourglass.invokeFactory('ExtropyHours','a',startDate=self.now-(self.h*2), endDate=self.now-self.h)
        #check that it is indeed 1
        self.assertEqual(self.timetracktool.searchResults()[0].workedHours, 1)
        # assert that only this one is in the catalog for today
        self.assertEqual(self.timetracktool.countIntervalHours( start=self.now -1, end=self.now ),1)

        #make one more hour, this one a day or two ago
        self.hourglass.invokeFactory('ExtropyHours','b',startDate=self.now-2, endDate=self.now - (2 + self.h))

        # then we query for only hours in the last 24 hours
        self.assertEqual(self.timetracktool.getHours( start=self.now -1, end=self.now )[0].workedHours,1)
        self.assertEqual(len(self.timetracktool.getHours( start=self.now -1, end=self.now )),1)

        self.assertEqual(self.timetracktool.countIntervalHours( start=self.now -1, end=self.now ),1)


class TestBudgeting(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.timetracktool = getattr(self.portal,TIMETOOLNAME)
        self.folder.invokeFactory('ExtropyProject','project',)
        self.project = self.folder.project
        self.project.invokeFactory('ExtropyPhase','phase')
        self.project.phase.invokeFactory('ExtropyFeature','requirement')
        self.project.phase.requirement.invokeFactory('ExtropyTask','t1')
        self.now = DateTime()
        self.h = 1.0/24.0

    def testBudgetGroups(self):
        self.project.phase.setBudgetCategory('Sales')
        self.assertEqual(self.project.phase.getBudgetCategory(),'Sales')
        self.timetracktool.addTimeTrackingHours( self.project.phase, 'foo', hours=1, start=None, end=None)
        hours =  self.timetracktool.getHours( node=self.project.phase)
        self.assertEqual(hours[0].workedHours,1)
        self.assertEqual(hours[0].getBudgetCategory,'Sales')




def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestExtropyHourSetup))
    suite.addTest(makeSuite(TestExtropyHours))
    suite.addTest(makeSuite(TestBudgeting))
    return suite

if __name__ == '__main__':
    framework()
