from Testing import ZopeTestCase
from Products.Extropy.tests import ExtropyTrackingTestCase

from Products.CMFPlone.utils import _createObjectByType

default_user = ZopeTestCase.user_name


class TestBase(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def testDefaultBudgetCategory(self):
        p = _createObjectByType('ExtropyProject', self.folder, 'project')
        self.assertEqual(p.getDefaultBudgetCategory(),'Billable')
        phase =_createObjectByType('ExtropyPhase', p, 'phase')
        self.assertEqual(phase.getDefaultBudgetCategory(),'Billable')
        p.setBudgetCategory('Sales')
        self.assertEqual(phase.getDefaultBudgetCategory(),'Sales')

    def testDefaultResponsible(self):
        project =_createObjectByType('ExtropyProject', self.folder, 'project')
        project.setProjectManager('foo')
        phase = _createObjectByType('ExtropyPhase', project, 'phase')
        self.assertEqual(phase.getDefaultResponsible(), 'foo')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBase))
    return suite
