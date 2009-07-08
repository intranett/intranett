#
# EXTask test
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.Extropy import config
from Interface.Verify import verifyObject

class TestInterfaces(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def testToolInterface(self):
        tool = getattr(self.portal, config.TOOLNAME)
        from Products.Extropy.interfaces import IExtropyTrackingTool
        self.failUnless(IExtropyTrackingTool.isImplementedBy(tool))
        self.failUnless(verifyObject(IExtropyTrackingTool, tool))

    def testTimeToolInterface(self):
        tool = getattr(self.portal, config.TIMETOOLNAME)
        from Products.Extropy.interfaces import IExtropyTimeTrackingTool
        self.failUnless(verifyObject(IExtropyTimeTrackingTool, tool))
        self.failUnless(IExtropyTimeTrackingTool.isImplementedBy(tool))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInterfaces))
    return suite
