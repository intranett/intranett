#
# EXTask test
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Interface.Verify import verifyObject
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

default_user = ZopeTestCase.user_name



class TestPlan(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # make a basic Project > Phase > Task - hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.project = self.folder.project
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.phase = self.folder.project.phase
        self.folder.project.phase.invokeFactory('ExtropyFeature','requirement')
        self.folder.project.phase.requirement.invokeFactory('ExtropyTask','task1')
        self.task1 = getattr(self.folder.project.phase.requirement,'task1')
        self.folder.invokeFactory('ExtropyPlan', 'plan')
        self.plan = self.folder.plan

    def testPlanInterface(self):
        from Products.Extropy.interfaces import IExtropyPlan
        self.failUnless(IExtropyPlan.isImplementedBy(self.plan))
        self.failUnless(verifyObject(IExtropyPlan, self.plan))

# test basic operations
# test task schema
# test task methods

    def testAddItem(self):
        pass
    def testDeleteItem(self):
        pass
    def testAddItemNotAllowed(self):
        pass
    def testAddAdditionalItem(self):
        pass
    def testdeleteAdditionalItem(self):
        pass
    def testGetItems(self):
        pass
    def testGetAdditionalItems(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPlan))
    return suite

if __name__ == '__main__':
    framework()
