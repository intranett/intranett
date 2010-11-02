import unittest2 as unittest

from AccessControl import getSecurityManager
from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.workflow.interfaces import ISharingPageRole
from zope.component import getUtilitiesFor

from intranett.policy.tests.base import IntranettTestCase


def checkPerm(permission, obj):
    sm = getSecurityManager()
    return sm.checkPermission(permission, obj)


class TestWorkflowSetup(IntranettTestCase):

    def setUp(self):
        portal = self.layer['portal']
        self.wftool = getToolByName(portal, 'portal_workflow')

    def test_workflow_assignments(self):
        portal = self.layer['portal']
        ttool = getToolByName(portal, 'portal_types')
        no_workflow = set([
            'ATBooleanCriterion', 'ATCurrentAuthorCriterion',
            'ATDateCriteria', 'ATDateRangeCriterion', 'ATListCriterion',
            'ATPathCriterion', 'ATPortalTypeCriterion', 'ATReferenceCriterion',
            'ATRelativePathCriterion', 'ATSelectionCriterion',
            'ATSimpleIntCriterion', 'ATSimpleStringCriterion',
            'ATSortCriterion', 'FieldsetFolder', 'FormBooleanField',
            'FormCaptchaField', 'FormCustomScriptAdapter', 'FormDateField',
            'FormFileField', 'FormFixedPointField', 'FormIntegerField',
            'FormLabelField', 'FormLikertField', 'FormLinesField',
            'FormMailerAdapter', 'FormMultiSelectionField',
            'FormPasswordField', 'FormRichLabelField', 'FormRichTextField',
            'FormSaveDataAdapter', 'FormSelectionField', 'FormStringField',
            'FormTextField', 'FormThanksPage', 'Plone Site',
        ])
        for type_ in no_workflow:
            wf = self.wftool.getChainForPortalType(type_)
            self.assertEquals(wf, (),
                              'Found workflow %s for type %s, expected '
                              '(), ' % (wf, type_))

        workflows = {
            'Discussion Item': ('one_state_workflow', ),
            'File': (),
            'Image': (),
        }
        for type_ in set(ttool.keys()) - no_workflow:
            wf = self.wftool.getChainForPortalType(type_)
            expected = workflows.get(type_, ('intranett_workflow', ))
            self.assertEquals(wf, expected,
                              'Found workflow %s for type %s, expected '
                              '%s, ' % (wf, type_, expected))

    @unittest.expectedFailure
    def test_sharing_page_roles(self):
        utilities = list(getUtilitiesFor(ISharingPageRole))
        names = [name for name, util in utilities]
        self.assertEquals(set(names),
                          set([u'Contributor', u'Editor', u'Reader']))


class TestWorkflowPermissions(IntranettTestCase):

    def test_no_anonymous_view_portal(self):
        logout()
        portal = self.layer['portal']
        self.assertFalse(checkPerm('View', portal['test-folder']))
        # We don't want this, but we first need to make sure the login form
        # and standard error message views work without anon View permission
        # on the portal object
        self.assertTrue(checkPerm('View', portal))

    def test_no_anonymous_view_new_page(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Document', 'doc1')
        doc1 = portal.doc1
        logout()
        self.assertFalse(checkPerm('View', doc1))

    def test_no_anonymous_view_new_folder(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Folder', 'folder1')
        folder1 = portal.folder1
        logout()
        self.assertFalse(checkPerm('View', folder1))


class TestWorkflowTransitions(IntranettTestCase):

    def setUp(self):
        portal = self.layer['portal']
        self.wftool = getToolByName(portal, 'portal_workflow')
        _doAddUser = aq_get(portal, 'acl_users')._doAddUser
        _doAddUser('member', 'secret', ['Member'], [])
        _doAddUser('manager', 'secret', ['Manager'], [])
        _doAddUser('editor', 'secret', ['Editor'], [])
        _doAddUser('reader', 'secret', ['Reader'], [])

        folder = portal['test-folder']
        folder.invokeFactory('Document', id='doc')
        self.doc = folder.doc

    def test_owner_publish_and_hide(self):
        self.assertEqual(self.wftool.getInfoFor(self.doc, 'review_state'),
                         'private')
        self.wftool.doActionFor(self.doc, 'publish')
        self.assertEqual(self.wftool.getInfoFor(self.doc, 'review_state'),
                         'published')
        self.wftool.doActionFor(self.doc, 'hide')
        self.assertEqual(self.wftool.getInfoFor(self.doc, 'review_state'),
                         'private')

    def _check_edit(self, user):
        if user is None:
            logout()
        else:
            login(self.layer['portal'], user)
        return checkPerm('Modify portal content', self.doc)

    def test_edit_permission_private(self):
        self.assertEqual(self.wftool.getInfoFor(self.doc, 'review_state'),
                         'private')

        self.assertFalse(self._check_edit('member'))
        self.assertTrue(self._check_edit('manager'))
        self.assertTrue(self._check_edit('editor'))
        self.assertFalse(self._check_edit('reader'))
        self.assertFalse(self._check_edit(None))

    def test_edit_permission_published(self):
        self.wftool.doActionFor(self.doc, 'publish')
        self.assertEqual(self.wftool.getInfoFor(self.doc, 'review_state'),
                         'published')

        self.assertFalse(self._check_edit('member'))
        self.assertTrue(self._check_edit('manager'))
        self.assertTrue(self._check_edit('editor'))
        self.assertFalse(self._check_edit('reader'))
        self.assertFalse(self._check_edit(None))

    def _check_view(self, user):
        if user is None:
            logout()
        else:
            login(self.layer['portal'], user)
        view = checkPerm('View', self.doc)
        access = checkPerm('Access contents information', self.doc)
        return view and access

    def test_view_permission_private(self):
        self.assertEqual(self.wftool.getInfoFor(self.doc, 'review_state'),
                         'private')

        self.assertFalse(self._check_view('member'))
        self.assertTrue(self._check_view('manager'))
        self.assertTrue(self._check_view('editor'))
        self.assertTrue(self._check_view('reader'))
        self.assertFalse(self._check_view(None))

    def test_view_permission_published(self):
        self.wftool.doActionFor(self.doc, 'publish')
        self.assertEqual(self.wftool.getInfoFor(self.doc, 'review_state'),
                         'published')

        self.assertTrue(self._check_view('member'))
        self.assertTrue(self._check_view('manager'))
        self.assertTrue(self._check_view('editor'))
        self.assertTrue(self._check_view('reader'))
        self.assertFalse(self._check_view(None))


class TestSitePermissions(IntranettTestCase):

    def test_disallow_sendto(self):
        logout()
        portal = self.layer['portal']
        self.assertFalse(checkPerm('Allow sendto', portal))
