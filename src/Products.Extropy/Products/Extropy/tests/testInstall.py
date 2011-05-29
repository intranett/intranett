#
# EXTask test
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase


class TestSetup(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        pass

    def testDummy(self):
        pass

    def testSkins(self):
        skins = self.portal.portal_skins.objectIds()
        self.failUnless('extropy_images' in skins)
        self.failUnless('extropy_templates' in skins)

    def testPortalTypes(self):
        types = self.portal.portal_types.objectIds()
        self.failUnless('ExtropyProject' in types)
        self.failUnless('ExtropyPhase' in types)
        self.failUnless('ExtropyActivity' in types)

    def testToolsInstalled(self):
        # Test something
        self.failUnless('extropy_tracking_tool' in self.portal.objectIds())
        self.failUnless('extropy_timetracker_tool' in self.portal.objectIds())

    def testAddingProject(self):
        # test that we can add a project
        self.folder.invokeFactory('ExtropyProject','project', title="project")
        self.failUnless('project' in self.folder.objectIds())
        self.assertEqual(self.folder.project.Title(), 'project')

    def testAddingPhase(self):
        # test that we can add a phase
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase1', title="phase")
        self.failUnless('phase1' in self.folder.project.objectIds())
        self.assertEqual(self.folder.project.phase1.Title(), 'phase')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
