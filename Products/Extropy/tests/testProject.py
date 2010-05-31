#
# Project test
#

from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFCore.utils import getToolByName
from DateTime import DateTime


class TestProject(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.folder.invokeFactory('ExtropyProject','project')
        self.project = self.folder.project

    def testProjectInterface(self):
        from Products.Extropy.interfaces import IExtropyBase
        self.failUnless(IExtropyBase.providedBy(self.project))
        from Products.Extropy.interfaces import IExtropyTracking
        self.failUnless(IExtropyTracking.providedBy(self.project))

    def testActivePhase(self):
        self.failUnlessEqual(self.folder.project.getActivePhases(), [])
        self.folder.project.invokeFactory('ExtropyPhase','phase1', startDate=DateTime()-10, endDate=DateTime()+10)
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.doActionFor(self.folder.project.phase1, 'activate')
        self.failUnlessEqual(len(self.folder.project.getActivePhases()),1)
        self.failUnlessEqual(self.folder.project.getActivePhases()[0].getId(), 'phase1')

        wftool.doActionFor(self.folder.project.phase1, 'close')
        self.failUnlessEqual(self.folder.project.getActivePhases(), [])

    def testAvailableParticipants(self):
        participants = self.project.getAvailableParticipants()
        self.failUnlessEqual(participants, ['test_user_1_'])

    def testProjectFolders(self):
        # test the auto-population works
        self.failUnless('project' in self.folder.objectIds())

    def testgetRequirementsByState(self):
        self.project.invokeFactory('ExtropyPhase','phase')
        self.project.phase.invokeFactory('ExtropyFeature','requirement1')
        rs =  self.project.phase.getRequirementsByState()
        self.assertEqual(len(rs),1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProject))
    return suite
