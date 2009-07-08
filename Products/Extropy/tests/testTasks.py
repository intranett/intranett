#
# ExtropyTask test
#

from DateTime import DateTime

from Testing import ZopeTestCase
from Interface.Verify import verifyObject
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
        self.failUnless(IExtropyTask.isImplementedBy(self.task1))
        self.failUnless(verifyObject(IExtropyTask, self.task1))

    def testTaskPriority(self):
        self.assertEqual(self.task1.getPriority(),5)
        self.task1.setPriority(10)
        self.assertEqual(self.task1.getPriority(),10)

    def testTaskInvokeFactoryPassesKeywords(self):
        self.folder.project.phase.requirement.invokeFactory('ExtropyTask','taskx', RESPONSE=None, title='test',estimatedDuration=5.0)
        #self.folder.project.phase.taskx.setEstimatedDuration(5.0)
        self.failUnless(self.folder.project.phase.requirement.taskx)
        self.assertEqual(self.folder.project.phase.requirement.taskx.getId(),'taskx')
        self.assertEqual(self.folder.project.phase.requirement.taskx.Title(),'test')
        self.assertEqual(self.folder.project.phase.requirement.taskx.getEstimatedDuration(), 5.0)

    def testTaskEstimatedDuration(self):
        self.folder.project.phase.requirement.invokeFactory('ExtropyTask','taskx', RESPONSE=None, title='test',estimatedDuration=5.0)
        #self.folder.project.phase.taskx.setEstimatedDuration(5.0)
        self.failUnless(self.folder.project.phase.requirement.taskx)
        self.assertEqual(self.folder.project.phase.requirement.taskx.getId(),'taskx')
        self.assertEqual(self.folder.project.phase.requirement.taskx.Title(),'test')
        self.assertEqual(self.folder.project.phase.requirement.taskx.getEstimatedDuration(), 5.0)

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

    def testTaskCreatesHistory(self):
        self.failUnlessEqual(len(self.task1.objectIds()),0)
        self.portal.portal_workflow.doActionFor(self.task1, 'claim')
        self.failUnlessEqual(len(self.task1.objectIds()),1)
        self.task1.processForm(values={'title':'confuse-a-cat'})
        self.failUnlessEqual(len(self.task1.objectIds()),2)
        self.failUnlessEqual( self.task1.Title(), 'confuse-a-cat' )

        hist = self.task1.objectValues()[-1]
        changes = hist.getChanges()
        self.failUnless(changes[0]['field'] == 'title')
        self.failUnlessEqual(changes[0]['to'], 'confuse-a-cat')

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

    def testTaskCommentfromREQUEST(self):
        self.app.REQUEST.form={}
        self.app.REQUEST.form['changenote']='CHANGED!'
        self.app.REQUEST.form['title']='confuse-a-cat'
        self.app.REQUEST.form['participants']='extropy'
        self.portal.portal_workflow.doActionFor(self.task1, 'claim')
        self.task1.processForm(REQUEST=self.app.REQUEST)
        self.failUnless(len(self.task1.objectIds())>0)
        self.failIf(self.task1.getChangenote())
        self.assertEqual(self.task1.objectValues()[-1].getChangenote(),"<p>CHANGED!</p>")
        self.assertEqual(self.task1.objectValues()[-1].Title(),"CHANGED!")
        self.failUnlessEqual( self.task1.Title(), 'confuse-a-cat' )
        self.failUnless( 'extropy' in self.task1.getParticipants() )

    def testSplitTask(self):
        self.task1.splitTask()
        splittasks = self.task1.getSplitTasks()
        self.failUnless(splittasks)
        self.failUnlessEqual(len(splittasks), 1)
        self.failUnlessEqual(splittasks[0].getOriginatingTask(), self.task1 )
        self.failIfEqual(splittasks[0].getId(), self.task1.getId())
        self.failIfEqual(splittasks[0], self.task1)

    def testSplittingTaskKeepsFeatureReference(self):
        self.phase.invokeFactory('ExtropyFeature','f1')
        f1 = self.phase.f1
        f1.invokeFactory('ExtropyTask','task1')
        t1 = f1.task1
        t2 = t1.splitTask()
        self.assertEqual( t1.getOriginatingFeature() , t2.getOriginatingFeature() )
        self.assertEqual( t1.getOriginatingFeature() , f1 )

    def testSplittingTaskKeepsValues(self):
        self.phase.invokeFactory('ExtropyFeature','f1')
        f1 = self.phase.f1
        f1.invokeFactory('ExtropyTask','task1')
        t1 = f1.task1
        t1.setResponsiblePerson('sam')
        t1.setParticipants(('sam','joe','ted'))
        self.assertEqual(t1.getResponsiblePerson(),'sam')
        t2 = t1.splitTask()
        self.assertEqual( t1.getParticipants() , t2.getParticipants() )
        self.assertEqual( t1.getResponsiblePerson() , t2.getResponsiblePerson() )

    def testSplittingTaskTwice(self):
        self.task1.splitTask()
        from zExceptions import BadRequest
        try:
            self.task1.splitTask()
        except BadRequest:
            self.fail()

    def testRemainingTimeinCatalog(self):
        self.task1.setEstimatedDuration(10)
        self.task1.reindexObject()
        self.assertEqual(self.task1.getEstimatedDuration(), 10)
        res = self.portal.extropy_tracking_tool.localQuery(self.portal,REQUEST=None, getId='task1')
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].getEstimatedDuration,10)

    def testRemainingTime(self):
        self.task1.setEstimatedDuration(10)
        self.task1.reindexObject()
        self.assertEqual(self.task1.getEstimatedDuration(), 10)
        self.assertEqual(self.task1.getRemainingTime(), 10)

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
