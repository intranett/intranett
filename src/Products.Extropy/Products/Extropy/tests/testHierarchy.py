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

    def testGetExtropyParent(self):
        self.assertEqual(self.phase.getExtropyParent(), self.project)

    def testPeoplePropagation(self):
        members = ('Albatross','Parrot')

        self.project.setParticipants(members)
        #if nothing is selected, let the selection trickle down
        self.assertEqual(self.project.getParticipants(),members)
        self.assertEqual(self.phase.getParticipants(),members)
        self.assertEqual(self.phase.getAvailableParticipants(),members)

    def testPeoplePropagation2(self):
        members = ('Albatross','Parrot','Fish')
        self.project.setParticipants(members)
        self.assertEqual(self.phase.getParticipants(),members)
        self.assertEqual(self.phase.getAvailableParticipants(),members)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestHierarchy))
    return suite
