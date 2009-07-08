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


class TestFeaturelist(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # set up a Feature/Tasks hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase1')
        #self.featurelist = getattr(self.folder.project, 'features')
        self.folder.project.phase1.invokeFactory('ExtropyFeature','feature1')
        feature = getattr(self.folder.project.phase1, 'feature1')
        feature.spawnTask()
        feature.spawnTask()
        self.featurelist.invokeFactory('ExtropyFeature','feature2')
        feature = getattr(self.folder.project.phase1, 'feature2')
        t = feature.spawnTask()
        t.splitTask()

    def testGetFeatures(self):
        features = self.featurelist.getFeatures()
        self.failUnlessEqual(len(features), 2)

    def testGetFeaturesWithTasks(self):
        features = self.featurelist.getFeaturesWithTasks()
        self.failUnlessEqual(len(features), 2)
        self.failUnlessEqual(len(features[0]['tasks']), 2)
        self.failUnlessEqual(len(features[1]['tasks']), 2)

    def testGetOpenFeatures(self):
        features = self.featurelist.getOpenFeatures()
        self.failUnlessEqual(len(features), 2)
        self.portal.portal_workflow.doActionFor(self.featurelist.feature1, 'discard')
        features = self.featurelist.getOpenFeatures()
        self.failUnlessEqual(len(features), 1)

    def testGetRemainingTime(self):
        self.assertEqual( self.featurelist.getRemainingTime(), 0 )
        t1 = self.featurelist.getFeatures()[0].getObject().getSpawnedTasks()[0]
        t1.setEstimatedDuration(3)
        t1.reindexObject()
        self.featurelist.getFeatures()[0].getObject().reindexObject()
        self.assertEqual( self.featurelist.getRemainingTime(), 3 )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFeaturelist))
    return suite

if __name__ == '__main__':
    framework()
