#
# EXTask test
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase


class TestFeatures(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # make a basic Project > Phase > Task - hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature')
        self.feature = getattr(self.folder.project.phase,'feature')

    def testAvailablePeople(self):
        self.folder.project.setParticipants(['joe','noob'])
        self.assertEqual(self.folder.project.phase.getAvailableParticipants(), self.folder.project.getParticipants())
        self.assertEqual(self.folder.project.phase.feature.getAvailableParticipants(), self.folder.project.getParticipants())

    def testfeatureCreatesHistory(self):
        self.failUnlessEqual(len(self.feature.objectIds()),0)
        self.feature.processForm(values={'title':'confuse-a-cat'})
        self.failUnlessEqual(len(self.feature.objectIds()),1)
        self.failUnless( self.feature.Title() == 'confuse-a-cat' )

        hist = self.feature.objectValues()[0]
        changes = hist.getChanges()
        self.failUnless(changes[0]['field'] == 'title')
        self.failUnless(changes[0]['to'] == 'confuse-a-cat')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFeatures))
    return suite
