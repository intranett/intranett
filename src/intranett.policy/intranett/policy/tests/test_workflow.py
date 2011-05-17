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

    def test_workflow_assignments(self):
        portal = self.layer['portal']
        wftool = getToolByName(portal, 'portal_workflow')
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
            wf = wftool.getChainForPortalType(type_)
            self.assertEquals(wf, (),
                              'Found workflow %s for type %s, expected '
                              '(), ' % (wf, type_))

        workflows = {
            'Discussion Item': ('one_state_workflow', ),
            'File': (),
            'Image': (),
        }
        for type_ in set(ttool.keys()) - no_workflow:
            wf = wftool.getChainForPortalType(type_)
            expected = workflows.get(type_, ('intranett_workflow',))
            self.assertEquals(wf, expected,
                              'Found workflow %s for type %s, expected '
                              '%s, ' % (wf, type_, expected))

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
        setRoles(portal, TEST_USER_ID, ['Member', 'Site Administrator'])
        portal.invokeFactory('Document', 'doc1')
        doc1 = portal.doc1
        logout()
        self.assertFalse(checkPerm('View', doc1))

    def test_no_anonymous_view_new_folder(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Member', 'Site Administrator'])
        portal.invokeFactory('Folder', 'folder1')
        folder1 = portal.folder1
        logout()
        self.assertFalse(checkPerm('View', folder1))


class TestSitePermissions(IntranettTestCase):

    def test_disallow_sendto(self):
        logout()
        portal = self.layer['portal']
        self.assertFalse(checkPerm('Allow sendto', portal))


class TestWorkflowTransitions(IntranettTestCase):

    def setUp(self):
        super(TestWorkflowTransitions, self).setUp()
        portal = self.layer['portal']
        addUser = aq_get(portal, 'acl_users').userFolderAddUser
        addUser('member', 'secret', ['Member'], [])
        addUser('admin', 'secret', ['Member', 'Site Administrator'], [])
        addUser('editor', 'secret', ['Editor'], [])
        addUser('reader', 'secret', ['Reader'], [])

        folder = portal['test-folder']
        folder.invokeFactory('Document', id='doc')

    def test_owner_publish_and_hide(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'private')
        wftool.doActionFor(doc, 'publish')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'published')
        wftool.doActionFor(doc, 'hide')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'private')

    def _check_edit(self, user):
        if user is None:
            logout()
        else:
            login(self.layer['portal'], user)
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        return checkPerm('Modify portal content', doc)

    def test_edit_permission_private(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'private')

        self.assertFalse(self._check_edit('member'))
        self.assertTrue(self._check_edit('admin'))
        self.assertTrue(self._check_edit('editor'))
        self.assertFalse(self._check_edit('reader'))
        self.assertFalse(self._check_edit(None))

    def test_edit_permission_published(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(doc, 'publish')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'published')

        self.assertFalse(self._check_edit('member'))
        self.assertTrue(self._check_edit('admin'))
        self.assertTrue(self._check_edit('editor'))
        self.assertFalse(self._check_edit('reader'))
        self.assertFalse(self._check_edit(None))

    def _check_view(self, user):
        portal = self.layer['portal']
        if user is None:
            logout()
        else:
            login(portal, user)
        doc = portal['test-folder'].doc
        view = checkPerm('View', doc)
        access = checkPerm('Access contents information', doc)
        return view and access

    def test_view_permission_private(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'), 'private')

        self.assertFalse(self._check_view('member'))
        self.assertTrue(self._check_view('admin'))
        self.assertTrue(self._check_view('editor'))
        self.assertTrue(self._check_view('reader'))
        self.assertFalse(self._check_view(None))

    def test_view_permission_published(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(doc, 'publish')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'published')

        self.assertTrue(self._check_view('member'))
        self.assertTrue(self._check_view('admin'))
        self.assertTrue(self._check_view('editor'))
        self.assertTrue(self._check_view('reader'))
        self.assertFalse(self._check_view(None))
