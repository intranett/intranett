#
# EXTask test
#

import transaction

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase


class TestFeatures(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # make a basic Project > Phase > Task - hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.folder.project.phase.invokeFactory('ExtropyFeature','feature')
        self.feature = getattr(self.folder.project.phase,'feature')

    def testFeatureInterface(self):
        from Products.Extropy.interfaces import IExtropyBase
        self.failUnless(IExtropyBase.providedBy(self.feature))
        from Products.Extropy.interfaces import IExtropyTracking
        self.failUnless(IExtropyTracking.providedBy(self.feature))

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

    def testMoveTo(self):
        self.folder.project.invokeFactory('ExtropyPhase','phase2')
        transaction.get().savepoint()
        feature = self.folder.project.phase.feature
        oldpath = feature.getPhysicalPath()
        self.failUnless('phase2' in self.folder.project.objectIds())
        self.failIf(self.folder.project.phase2.objectIds())
        feature.moveTo(self.folder.project.phase2.UID())
        self.failIf(self.folder.project.phase.objectIds())
        self.failUnless('feature' in self.folder.project.phase2.objectIds())
        newpath = feature.getPhysicalPath()
        self.failIfEqual(oldpath, newpath)

    def testMoveToViaProcessForm(self):
        self.folder.project.invokeFactory('ExtropyPhase','phase2')
        transaction.get().savepoint()
        feature = self.folder.project.phase.feature
        oldpath = feature.getPhysicalPath()
        self.failUnless('phase2' in self.folder.project.objectIds())
        self.failUnless('feature' in self.folder.project.phase.objectIds())
        self.failIf(self.folder.project.phase2.objectIds())
        self.app.REQUEST.form={}
        self.app.REQUEST.form['moveToPhase']=self.folder.project.phase2.UID()
        feature.processForm()
        self.failIf(self.folder.project.phase.objectIds())
        self.failUnless('feature' in self.folder.project.phase2.objectIds())
        newpath = feature.getPhysicalPath()
        self.failIfEqual(oldpath, newpath)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFeatures))
    return suite
