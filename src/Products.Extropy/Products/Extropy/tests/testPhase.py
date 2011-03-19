#
# EXTask test
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase


class TestPhase(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # set up a Feature/Tasks hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.phase = self.folder.project.phase

    def testPhaseInterface(self):
        from Products.Extropy.interfaces import IExtropyBase
        self.failUnless(IExtropyBase.providedBy(self.phase))
        from Products.Extropy.interfaces import IExtropyTracking
        self.failUnless(IExtropyTracking.providedBy(self.phase))

    def testGettingRequirements(self):
        self.phase.invokeFactory('ExtropyFeature','r1')
        self.assertEqual(len(self.phase.getDeliverables()),1)
        self.assertEqual(self.phase.getDeliverables()[0].getObject(),getattr(self.phase,'r1'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPhase))
    return suite
