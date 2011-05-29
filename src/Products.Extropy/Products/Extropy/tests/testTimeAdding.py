#
# ExtropyTrackingTestCase Skeleton
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from DateTime import DateTime
from Products.Extropy.config import TIMETOOLNAME
from Products.CMFPlone.utils import _createObjectByType


class TestTimeAdding(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.hour = 1.0/24.0
        self.tool = getattr(self.portal, TIMETOOLNAME)

    def testGettingTimeTackableParent(self):
        # Only tasks and activitites are time trackable
        self.folder.invokeFactory('ExtropyProject','project1')
        project = self.folder.project1
        self.assertEqual(self.tool.findTimeTrackableParent(project), None)
        self.folder.project1.invokeFactory('ExtropyPhase', 'p1')

    def testConvertHours(self):
        self.assertEqual(self.tool.convertHours(1), (1.0/24.0))
        self.assertEqual(self.tool.convertHours(0), 0)
        self.assertEqual(self.tool.convertHours(24),1)

    def testGetLastRegisteredTime(self):
        _createObjectByType('ExtropyHourGlass',self.folder, 'hourglass')
        self.folder.hourglass.invokeFactory('ExtropyHours','bluh')
        self.tool.addTimeTrackingHours( self.folder,'testHours', 1 )
        self.failUnlessEqual(self.folder.hourglass.objectValues('ExtropyHours')[-1].end(), self.tool.getLastRegisteredTime())

    def testAddingTime(self):
        self.folder.invokeFactory('ExtropyProject','project1')
        p1 = self.folder.project1
        self.tool.addTimeTrackingHours( p1,'testHours', 1 )



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTimeAdding))
    return suite
