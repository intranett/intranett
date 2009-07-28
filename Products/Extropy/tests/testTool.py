#
# ExtropyTrackingTestCase Skeleton
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFPlone.utils import _createObjectByType

from DateTime import DateTime


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

    def testCatalogingTask(self):
        self.setRoles(['Manager'])
        self.failUnlessEqual(len(self.tool()),0)
        _createObjectByType('ExtropyTask', self.portal, 'task')
        self.failUnless(len(self.tool())>0)

    def testCatalogingUsesRightCatalog(self):
        self.setRoles(['Manager'])
        self.assertEqual(len(self.tool()), 0)
        _createObjectByType('ExtropyTask', self.portal, 'task')
        #the tracktool should have one entry from the task
        self.assertEqual(len(self.tool()), 1)

    def testLocalQueries(self):
        self.setRoles(['Manager'])
        _createObjectByType('ExtropyTask', self.portal, 'task')
        self.portal.invokeFactory('Folder','taskfolder')
        _createObjectByType('ExtropyTask', self.portal.taskfolder, 'subtask')
        self.failUnlessEqual(len(self.tool.localQuery(node=self.portal)),2)
        self.failUnlessEqual(len(self.tool.localQuery(node=self.portal.taskfolder)),1)

    def testTrackingQuery(self):
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature')

        self.folder.project.phase.feature.invokeFactory('ExtropyTask','task0')
        self.folder.project.phase.feature.invokeFactory('ExtropyTask','task1')

        self.folder.project.invokeFactory('ExtropyPhase','phase2')
        self.folder.project.phase2.invokeFactory('ExtropyFeature','feature')
        self.folder.project.phase2.feature.invokeFactory('ExtropyTask','task2')

        self.assertEqual(len(self.tool.trackingQuery(self.folder.project, portal_type='ExtropyTask')), 3)

        self.assertEqual(len(self.tool.trackingQuery(self.folder.project.phase, portal_type='ExtropyTask')), 2)

        self.assertEqual(len(self.tool.trackingQuery(self.folder.project.phase.feature, portal_type='ExtropyTask')), 2)
        self.assertEqual(len(self.tool.trackingQuery(self.folder.project.phase2.feature, portal_type='ExtropyTask')), 1)

    def testSummingEstimates(self):
        # We'll add some tasks and test that they can be properly summed up
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature')
        today = DateTime().earliestTime()
        self.folder.project.phase.feature.invokeFactory('ExtropyTask','task0',estimatedDuration=1)
        self.folder.project.phase.feature.invokeFactory('ExtropyTask','task1',estimatedDuration=3)
        tasks = self.tool.searchResults(portal_type='ExtropyTask')
        sum = self.tool.sumEstimates(tasks)
        self.assertEqual(sum, 4)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTool))
    return suite
