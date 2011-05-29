from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase


class TestTool(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.tool = self.portal.extropy_tracking_tool

    def testToolInstalls(self):
        # Test something
        self.failUnless('extropy_tracking_tool' in self.portal.objectIds())

    def testIndexesSetupRight(self):
        self.failIf('id' in self.tool.indexes())

    def testMetadataSetupRight(self):
        self.failIf('id' in self.tool.schema())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTool))
    return suite
