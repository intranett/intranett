#
# EXTask test
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

default_user = ZopeTestCase.user_name


class TestScripts(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def afterSetUp(self):
        pass

    def testPrintingDuration(self):
        self.assertEqual(self.portal.printDuration(1),'an hour')
        self.assertEqual(self.portal.printDuration(2),'2 hours')
        self.assertEqual(self.portal.printDuration(3),'half a day')
        self.assertEqual(self.portal.printDuration(4),'half a day')
        self.assertEqual(self.portal.printDuration(5),'a day')
        self.assertEqual(self.portal.printDuration(6),'a day')
        self.assertEqual(self.portal.printDuration(7),'a day')
        self.assertEqual(self.portal.printDuration(8),'1 1/2 days')
        self.assertEqual(self.portal.printDuration(9),'1 1/2 days')
        self.assertEqual(self.portal.printDuration(12),'2 days')
        self.assertEqual(self.portal.printDuration(14),'2 1/2 days')
        self.assertEqual(self.portal.printDuration(30),'a week')
        self.assertEqual(self.portal.printDuration(60),'2 weeks')
        self.assertEqual(self.portal.printDuration(63),'2 weeks')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestScripts))
    return suite

if __name__ == '__main__':
    framework()
