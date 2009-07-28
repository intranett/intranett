#
# Extropy workflow tests
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

default_user = ZopeTestCase.user_name


class TestTaskWorkflow(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','deliverable')
        self.deliverable = self.folder.project.phase.deliverable

    def testWorkflowInstalled(self):
        self.failUnless('extropy_task_workflow' in self.portal.portal_workflow.objectIds())

    def testWorkflowAssignedToTask(self):
        wf_tool = self.portal.portal_workflow
        self.failUnlessEqual(wf_tool.getChainForPortalType('ExtropyTask'), ('extropy_task_workflow',))

    def testInitialState(self):
        wf_tool = self.portal.portal_workflow
        self.deliverable.invokeFactory('ExtropyTask','task')
        task = self.deliverable.task
        self.failUnlessEqual(wf_tool.getInfoFor(task, 'review_state'), 'unassigned')

    def testSetResponsible(self):
        wf_tool = self.portal.portal_workflow
        self.deliverable.invokeFactory('ExtropyTask','task')
        task = self.deliverable.task
        task.setResponsiblePerson(default_user)
        self.failUnlessEqual(wf_tool.getInfoFor(task, 'review_state'), 'assigned')
        self.failUnlessEqual(str(task.getResponsiblePerson()), default_user)


class TestFeatureWorkflow(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.setRoles(['Manager'])

    def testWorkflowInstalled(self):
        self.failUnless('extropy_feature_workflow' in self.portal.portal_workflow.objectIds())

    def testWorkflowScriptsInstalled(self):
        wfscripts = self.portal.portal_workflow.extropy_feature_workflow.scripts
        scriptids = wfscripts.objectIds()
        self.failUnlessEqual(len(scriptids), 1)

    def testWorkflowAssignedToFeature(self):
        wf_tool = self.portal.portal_workflow
        self.failUnlessEqual(wf_tool.getChainForPortalType('ExtropyFeature'), ('extropy_feature_workflow',))

    def testInitialState(self):
        wf_tool = self.portal.portal_workflow
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature1')
        feature = self.folder.project.phase.feature1
        self.failUnlessEqual(wf_tool.getInfoFor(feature, 'review_state'), 'open')

    def testDiscardAlsoDiscardstasks(self):
        wf_tool = self.portal.portal_workflow
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature1')
        feature = self.folder.project.phase.feature1

        feature.invokeFactory('ExtropyTask', 'task1')
        feature.invokeFactory('ExtropyTask', 'task2')
        feature.invokeFactory('ExtropyTask', 'task3')
        feature.invokeFactory('ExtropyTask', 'task4')

        # task 1 remains unassigned
        wf_tool.doActionFor(feature.task2, 'discard')
        wf_tool.doActionFor(feature.task3, 'complete')
        # setting the responsible auto-assign the task
        feature.task4.setResponsiblePerson(default_user)

        wf_tool.doActionFor(feature, 'discard')

        getState = lambda ob: wf_tool.getInfoFor(ob, 'review_state')
        self.failUnlessEqual(getState(feature.task1), 'discarded')
        self.failUnlessEqual(getState(feature.task2), 'discarded')
        self.failUnlessEqual(getState(feature.task3), 'completed')
        self.failUnlessEqual(getState(feature.task4), 'discarded')

    def testAllTasksComplete(self):
        wf_tool = self.portal.portal_workflow
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature1')
        feature = self.folder.project.phase.feature1

        feature.invokeFactory('ExtropyTask', 'task1')
        feature.invokeFactory('ExtropyTask', 'task2')
        feature.invokeFactory('ExtropyTask', 'task3')
        feature.invokeFactory('ExtropyTask', 'task4')

        # task 1 remains unassigned
        wf_tool.doActionFor(feature.task2, 'discard')
        wf_tool.doActionFor(feature.task3, 'complete')
        # setting the responsible auto-assign the task
        feature.task4.setResponsiblePerson(default_user)

        # setting task 1 to complete should not change anything, as task4 is
        # still assigned.
        wf_tool.doActionFor(feature.task1, 'complete')
        getState = lambda ob: wf_tool.getInfoFor(ob, 'review_state')
        self.assertEqual(getState(feature), 'open')

        # completing task4 should trigger the transition
        wf_tool.doActionFor(feature.task4, 'complete')
        self.assertEqual(getState(feature), 'taskscomplete')

    def testNoTasksCloseTransition(self):
        wf_tool = self.portal.portal_workflow
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature1')
        feature = self.folder.project.phase.feature1

        wf_actions = wf_tool.listActions(object=feature)
        action_ids = [a['id'] for a in wf_actions]
        self.assertTrue('empty_close' in action_ids)

        feature.invokeFactory('ExtropyTask', 'task1')

        wf_actions = wf_tool.listActions(object=feature)
        action_ids = [a['id'] for a in wf_actions]
        self.assertTrue('empty_close' not in action_ids)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTaskWorkflow))
    suite.addTest(makeSuite(TestFeatureWorkflow))
    return suite
