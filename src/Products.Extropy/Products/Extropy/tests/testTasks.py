#
# ExtropyTask test
#

from DateTime import DateTime

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

default_user = ZopeTestCase.user_name


class TestTasks(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # make a basic Project > Phase > Task - hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.project = self.folder.project
        self.folder.project.invokeFactory('ExtropyPhase','phase')
        self.phase = self.folder.project.phase
        self.folder.project.phase.invokeFactory('ExtropyFeature','requirement')
        self.folder.project.phase.requirement.invokeFactory('ExtropyTask','task1')
        self.task1 = getattr(self.folder.project.phase.requirement,'task1')

    def testTaskInterface(self):
        from Products.Extropy.interfaces import IExtropyTask
        self.failUnless(IExtropyTask.providedBy(self.task1))

    def testTaskPriority(self):
        self.assertEqual(self.task1.getPriority(),5)
        self.task1.setPriority(10)
        self.assertEqual(self.task1.getPriority(),10)

    def testTaskInvokeFactoryPassesKeywords(self):
        self.folder.project.phase.requirement.invokeFactory('ExtropyTask','taskx', RESPONSE=None, title='test')
        self.failUnless(self.folder.project.phase.requirement.taskx)
        self.assertEqual(self.folder.project.phase.requirement.taskx.getId(),'taskx')
        self.assertEqual(self.folder.project.phase.requirement.taskx.Title(),'test')

    def testGetTasks(self):
        self.failUnless(self.folder.project.getTasks())
        self.failUnless(self.folder.project.phase.getTasks())
        self.assertEqual(self.phase.getTasks()[0].getId, 'task1' )
        self.folder.project.invokeFactory('ExtropyPhase','phase2')
        self.failIf(self.folder.project.phase2.getTasks())

    def testGetCurrentUserTasks(self):
        self.failIf(self.folder.project.getTasksForCurrentUser())
        self.folder.project.phase.requirement.task1.setResponsiblePerson(default_user)
        self.folder.project.phase.requirement.task1.reindexObject()
        self.failUnless(self.folder.project.getTasksForCurrentUser())

    def testHistoryIsPartOfSearchableText(self):
        self.task1.processForm(values={'changenote':'ham and spam'})
        self.task1.processForm(values={'changenote':'eggs'})
        st = self.task1.SearchableText()
        self.failUnlessEqual(len(self.task1.objectIds()),2)
        self.failUnlessEqual(len(self.task1.getHistory()),2)
        self.failUnless('ham' in st)
        self.failUnless('spam' in st)
        self.failUnless('eggs' in st)

    def testTaskComment(self):
        self.task1.processForm(REQUEST=self.app.REQUEST, values={'changenote':'CHANGED!'})
        self.failUnless(len(self.task1.objectIds())>0)
        self.failIf(self.task1.getChangenote())
        self.assertEqual(self.task1.objectValues()[0].getChangenote(),"<p>CHANGED!</p>")

    def testAvailableDates(self):
        today = DateTime().earliestTime()
        expected = [(today + i) for i in range(22)]
        self.assertEqual(self.task1.getAvailableDates(), expected)

        start = DateTime('01/01/2000')
        self.phase.requirement.setStartDate(start)
        self.phase.requirement.setEndDate(DateTime('05/01/2000'))
        expected = [(start + i) for i in range(5)]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTasks))
    return suite
