#
# EXTask test
#

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase


class TestHierarchy(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        self.folder.invokeFactory('ExtropyProject','project')
        self.project = getattr(self.folder,'project')

        self.project.invokeFactory('ExtropyPhase','phase')
        self.phase = getattr(self.project,'phase')

        self.phase.invokeFactory('ExtropyFeature','deliverable')
        self.deliverable = getattr(self.phase,'deliverable')

        self.deliverable.invokeFactory('ExtropyTask','task')
        self.task = getattr(self.deliverable,'task')

    def testGetExtropyParent(self):
        self.assertEqual(self.phase.getExtropyParent(), self.project)
        self.assertEqual(self.task.getExtropyParent(), self.deliverable)

    def testGetExtropyParentWithMetaType(self):
        self.assertEqual(self.task.getExtropyParent(metatype='ExtropyProject'), self.project)
        self.assertEqual(self.task.getExtropyParent(metatype='ExtropyPhase'), self.phase)
        self.assertEqual(self.task.getExtropyParent(metatype=None), self.deliverable)
        self.assertEqual(self.task.getExtropyParent(metatype='FruitFly'), None)

    def testExtropyParentChain(self):
        chain = self.task.getExtropyParentChain()
        self.failUnless(self.project in chain)
        self.failUnless(self.phase in chain)
        self.failIf(self.task in chain)

    def testPeoplePropagation(self):
        members = ('Albatross','Parrot')

        self.project.setParticipants(members)
        #if nothing is selected, let the selection trickle down
        self.assertEqual(self.project.getParticipants(),members)
        self.assertEqual(self.phase.getParticipants(),members)
        self.assertEqual(self.phase.getAvailableParticipants(),members)
        self.assertEqual(self.task.getAvailableParticipants(),members)

    def testPeoplePropagation2(self):

        members = ('Albatross','Parrot','Fish')
        somemembers = ('Albatross','Fish')

        self.project.setParticipants(members)
        self.assertEqual(self.task.getAvailableParticipants(),members)

        self.assertEqual(self.phase.getParticipants(),members)
        self.assertEqual(self.phase.getAvailableParticipants(),members)

        #We limit the vocabulary at the phase level
        # this should change
        self.deliverable.setParticipants(somemembers)

        self.assertEqual(self.deliverable.getParticipants(),somemembers)
        self.assertEqual(self.deliverable.getAvailableParticipants(),members)

        self.assertEqual(self.task.getAvailableParticipants(),members)

        self.task.setParticipants(('Fish'))

        self.assertEqual(self.task.getParticipants(),('Fish',))
        self.assertEqual(self.task.getAvailableParticipants(),members)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestHierarchy))
    return suite
