import transaction
from DateTime import DateTime
from Products.CMFPlone.utils import _createObjectByType

from Products.Extropy.config import TIMETOOLNAME
from Products.Extropy.tests import ExtropyTrackingTestCase


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
        self.assertEquals(len(self.timetracktool()), 1)

    def testCatalogingHoursOnlyInTheTimeTrackTool(self):
        # test that hours get cataloged ONLY in the tool
        l = len( self.portal.portal_catalog() )
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass')
        # HourGlasses dont get cataloged anywhere
        self.folder.hourglass.invokeFactory('ExtropyHours','test')
        # the number of objects in the catalog should not increasae
        self.assertEquals(len(self.portal.portal_catalog()), l)


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

    def testMovingHours(self):
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass2')
        hourglass2 = getattr(self.folder, 'hourglass2')
        self.hourglass.invokeFactory('ExtropyHours', 'a', startDate=self.now-(self.h*2), endDate=self.now-self.h)
        transaction.savepoint(optimistic=True)
        hourglass2.manage_pasteObjects(self.hourglass.manage_cutObjects('a'))
        self.failUnless('a' in hourglass2)
        self.failIf('a' in self.hourglass)
        self.assertEquals(len(self.hourglass), 0)

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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestExtropyHourSetup))
    suite.addTest(makeSuite(TestExtropyHours))
    return suite
