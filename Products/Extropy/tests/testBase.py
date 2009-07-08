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

default_user = ZopeTestCase.user_name


class TestBase(ExtropyTrackingTestCase.ExtropyTrackingTestCase):

    def testParticipantsLocalRoles(self):
        base = _createObjectByType('ExtropyProject', self.folder, 'phase')
        uf = self.portal.acl_users
        userlist = (default_user,)
        self.failIf('Participant' in base.get_local_roles_for_userid(default_user))
        self.failIf('Participant' in uf.getUser(default_user).getRolesInContext(base))
        base.setParticipants(userlist)
        self.assertEqual(base.getParticipants(), userlist)
        self.failUnless('Participant' in base.get_local_roles_for_userid(default_user))
        self.failUnless('Participant' in uf.getUser(default_user).getRolesInContext(base))
        base.setParticipants([])
        self.assertEqual(base.getParticipants(), ())
        self.failIf('Participant' in base.get_local_roles_for_userid(default_user))
        self.failIf('Participant' in uf.getUser(default_user).getRolesInContext(base))

    def testGenerateUniqueId(self):
        proj = _createObjectByType('ExtropyProject', self.folder, 'project')
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'1')
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'2')
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'3')
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'4')
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'5')
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'6')
        self.failIfEqual(proj.generateUniqueId('Feature'),'7') # features do not have sequential ids
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'7')

        p1 = _createObjectByType('ExtropyPhase', self.folder.project, 'phase1')
        self.assertEqual(p1.generateUniqueId('ExtropyTask'),'8')
        self.assertEqual(proj.generateUniqueId('ExtropyTask'),'9')
        self.assertEqual(p1.generateUniqueId('ExtropyTask'),'10')

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
        feature = _createObjectByType('ExtropyFeature', phase, 'feature')
        self.assertEqual(feature.getDefaultResponsible(), 'foo')
        task = _createObjectByType('ExtropyTask', feature, 'task')
        self.assertEqual(task.getDefaultResponsible(), 'foo')
        # Out of context task
        task = _createObjectByType('ExtropyTask', self.folder, 'task')
        self.assertEqual(task.getDefaultResponsible(), None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBase))
    return suite

if __name__ == '__main__':
    framework()
