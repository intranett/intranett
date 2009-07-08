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


class TestBugs(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        # make a basic Project > Phase > Task - hierarchy
        self.folder.invokeFactory('ExtropyProject','project')
        self.folder.project.getBugJar().invokeFactory('ExtropyBug','bug1')
        self.bug = getattr(self.folder.project.getBugJar(),'bug1')

    def testBugCreatesHistory(self):
        self.failUnlessEqual(len(self.bug.objectIds()),0)
        self.bug.processForm(values={'title':'confuse-a-cat'})
        self.failUnlessEqual(len(self.bug.objectIds()),1)
        self.failUnless( self.bug.Title() == 'confuse-a-cat' )

        hist = self.bug.objectValues()[0]
        changes = hist.getChanges()
        self.failUnless(changes[0]['field'] == 'title')
        self.failUnless(changes[0]['to'] == 'confuse-a-cat')

    def testBugComment(self):
        self.bug.processForm(REQUEST=self.app.REQUEST, values={'changenote':'CHANGED!'})
        self.failUnless(len(self.bug.objectIds())>0)
        self.failIf(self.bug.getChangenote())
        self.assertEqual(self.bug.objectValues()[0].getChangenote(),"<p>CHANGED!</p>")

    def testTaskCommentfromREQUEST(self):
        self.app.REQUEST.form={}
        self.app.REQUEST.form['changenote']='CHANGED!'
        self.app.REQUEST.form['title']='confuse-a-cat'
        self.app.REQUEST.form['participants']='extropy'
        self.bug.processForm(REQUEST=self.app.REQUEST)
        self.failUnless(len(self.bug.objectIds())>0)
        self.failIf(self.bug.getChangenote())
        self.assertEqual(self.bug.objectValues()[0].getChangenote(),"<p>CHANGED!</p>")
        self.assertEqual(self.bug.objectValues()[0].Title(),"CHANGED!")
        self.failUnless( self.bug.Title() == 'confuse-a-cat' )


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBugs))
    return suite

if __name__ == '__main__':
    framework()
