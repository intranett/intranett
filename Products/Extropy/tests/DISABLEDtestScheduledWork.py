#
# EXTask test
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from DateTime import DateTime
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from DateTime import DateTime



class TestScheduledWork(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        pass

    def testAddingSchedule(self):
        _createObjectByType('ExtropyScheduledWork', self.folder, 'work')
        self.failUnless('work' in self.folder.objectIds())

    def testDuration(self):
        now = DateTime()
        hour = 1.0/24.0
        _createObjectByType('ExtropyScheduledWork', self.folder, 'work', startDate=now-(hour*2), endDate=now)
        w = self.folder.work
        self.failUnless(w.duration() == 2)




def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestScheduledWork))
    return suite

if __name__ == '__main__':
    framework()
