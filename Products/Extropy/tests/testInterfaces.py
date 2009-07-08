#
# EXTask test
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase


from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from Products.Extropy.config import *
from Interface.Verify import verifyObject

class TestInterfaces(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def testToolInterface(self):
        tool = getattr(self.portal, TOOLNAME)
        from Products.Extropy.interfaces import IExtropyTrackingTool
        self.failUnless(IExtropyTrackingTool.isImplementedBy(tool))
        self.failUnless(verifyObject(IExtropyTrackingTool, tool))

    def testTimeToolInterface(self):
        tool = getattr(self.portal, TIMETOOLNAME)
        from Products.Extropy.interfaces import IExtropyTimeTrackingTool
        self.failUnless(verifyObject(IExtropyTimeTrackingTool, tool))
        self.failUnless(IExtropyTimeTrackingTool.isImplementedBy(tool))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInterfaces))
    return suite

if __name__ == '__main__':
    framework()
