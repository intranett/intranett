#
# Project test
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Interface.Verify import verifyObject
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from DateTime import DateTime

class TestProject(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # set up a Feature/Tasks hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.project = self.folder.project

    def testProjectInterface(self):
        from Products.Extropy.interfaces import IExtropyBase
        self.failUnless(IExtropyBase.isImplementedBy(self.project))
        self.failUnless(verifyObject(IExtropyBase, self.project))
        from Products.Extropy.interfaces import IExtropyTracking
        self.failUnless(IExtropyTracking.isImplementedBy(self.project))
        self.failUnless(verifyObject(IExtropyTracking, self.project))

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

    def getTasks(self):
        self.project.invokeFactory('ExtropyPhase','phase')
        self.project.phase.invokeFactory('ExtropyFeature','requirement1')
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t1', title='fish')
        self.assertEqual(self.project.phase.requirement1.t1, self.project.getTasks()[0])
        self.assertEqual(self.project.phase.requirement1.t1.Title(), self.project.Title)

    def testGettingEstimates(self):
        self.project.invokeFactory('ExtropyPhase','phase')
        self.project.phase.invokeFactory('ExtropyFeature','requirement1')
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t1', estimatedDuration=5)

        self.assertEqual(self.project.getEstimates(),5)
        self.assertEqual(self.project.phase.getEstimates(),5)


# things to test for;
# getting tasks by keywords
# getTasksByState
# getTasksForCurrentUser
#



    def testCountingTasks(self):
        self.project.invokeFactory('ExtropyPhase','phase')
        self.project.phase.invokeFactory('ExtropyFeature','requirement1')
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t1', title='fish')
        self.assertEqual( self.project.countTasks(), 1)
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t2', title='fish')
        self.assertEqual( self.project.countTasks(), 2)
        self.assertEqual( self.project.phase.countTasks(), 2)
        self.assertEqual( self.project.phase.requirement1.countTasks(), 2)

    def testCountingOpenTasks(self):
        self.project.invokeFactory('ExtropyPhase','phase')
        self.project.phase.invokeFactory('ExtropyFeature','requirement1')
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t1', title='fish')
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t2', title='fish')
        self.assertEqual( self.project.countOpenTasks(), 2)
        self.portal.portal_workflow.doActionFor(self.project.phase.requirement1.t2, 'discard')
        self.assertEqual( self.project.countOpenTasks(), 1)

    def testCountingOpenTasksIsIndexed(self):
        self.project.invokeFactory('ExtropyPhase','phase')
        self.project.phase.invokeFactory('ExtropyFeature','requirement1')
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t1', title='fish')
        self.project.phase.requirement1.invokeFactory('ExtropyTask','t2', title='fish')
        self.portal.portal_workflow.doActionFor(self.project.phase.requirement1.t2, 'discard')
        d = self.project.getDeliverables()[0]
        self.assertEqual(d.countOpenTasks,1)
        self.assertEqual(d.countTasks,2)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProject))
    return suite

if __name__ == '__main__':
    framework()
