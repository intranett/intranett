from AccessControl import getSecurityManager
from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

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
            'Discussion Item': ('one_state_intranett_workflow', ),
            'File': ('two_state_intranett_workflow', ),
            'Image': ('two_state_intranett_workflow', ),
            'TeamWorkspace': ('workspace_workflow', ),
        }
        for type_ in set(ttool.keys()) - no_workflow:
            wf = wftool.getChainForPortalType(type_)
            expected = workflows.get(type_, ('intranett_workflow',))
            self.assertEquals(wf, expected,
                              'Found workflow %s for type %s, expected '
                              '%s, ' % (wf, type_, expected))


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

    def test_no_anonymous_view_new_file(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Member', 'Site Administrator'])
        portal.invokeFactory('File', 'file1')
        file1 = portal.file1
        logout()
        self.assertFalse(checkPerm('View', file1))

    def test_no_add_workspace_in_private_workspace(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Member', 'Site Administrator'])
        portal.invokeFactory('TeamWorkspace', 'team1')
        team1 = portal.team1
        self.assertFalse(checkPerm('intranett.policy: Add TeamWorkspace', team1))

    def test_no_add_workspace_in_public_workspace(self):
        portal = self.layer['portal']
        wftool = getToolByName(portal, 'portal_workflow')
        setRoles(portal, TEST_USER_ID, ['Member', 'Site Administrator'])
        portal.invokeFactory('TeamWorkspace', 'team1')
        team1 = portal.team1
        wftool.doActionFor(team1, 'publish')
        self.assertFalse(checkPerm('intranett.policy: Add TeamWorkspace', team1))


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

    def _check_edit(self, doc, user):
        portal = self.layer['portal']
        if user is None:
            logout()
        else:
            login(portal, user)
        return checkPerm('Modify portal content', doc)

    def test_edit_permission_private(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'private')

        self.assertFalse(self._check_edit(doc, 'member'))
        self.assertTrue(self._check_edit(doc, 'admin'))
        self.assertTrue(self._check_edit(doc, 'editor'))
        self.assertFalse(self._check_edit(doc, 'reader'))
        self.assertFalse(self._check_edit(doc, None))

    def test_edit_permission_published(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(doc, 'publish')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'published')

        self.assertFalse(self._check_edit(doc, 'member'))
        self.assertTrue(self._check_edit(doc, 'admin'))
        self.assertTrue(self._check_edit(doc, 'editor'))
        self.assertFalse(self._check_edit(doc, 'reader'))
        self.assertFalse(self._check_edit(doc, None))

    def _check_view(self, doc, user):
        portal = self.layer['portal']
        if user is None:
            logout()
        else:
            login(portal, user)
        view = checkPerm('View', doc)
        access = checkPerm('Access contents information', doc)
        return view and access

    def test_view_permission_private(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'), 'private')

        self.assertFalse(self._check_view(doc, 'member'))
        self.assertTrue(self._check_view(doc, 'admin'))
        self.assertTrue(self._check_view(doc, 'editor'))
        self.assertTrue(self._check_view(doc, 'reader'))
        self.assertFalse(self._check_view(doc, None))

    def test_view_permission_published(self):
        portal = self.layer['portal']
        doc = portal['test-folder'].doc
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(doc, 'publish')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'published')

        self.assertTrue(self._check_view(doc, 'member'))
        self.assertTrue(self._check_view(doc, 'admin'))
        self.assertTrue(self._check_view(doc, 'editor'))
        self.assertTrue(self._check_view(doc, 'reader'))
        self.assertFalse(self._check_view(doc, None))

    def test_file_edit_permission_published(self):
        portal = self.layer['portal']
        file_id = portal['test-folder'].invokeFactory('File', id='file')
        file = portal['test-folder'][file_id]
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(file, 'review_state'),
                         'published')

        self.assertFalse(self._check_edit(file, 'member'))
        self.assertTrue(self._check_edit(file, 'admin'))
        self.assertTrue(self._check_edit(file, 'editor'))
        self.assertFalse(self._check_edit(file, 'reader'))
        self.assertFalse(self._check_edit(file, None))

    def test_file_view_permission_published(self):
        portal = self.layer['portal']
        file_id = portal['test-folder'].invokeFactory('File', id='file')
        file = portal['test-folder'][file_id]
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(file, 'review_state'),
                         'published')

        self.assertTrue(self._check_view(file, 'member'))
        self.assertTrue(self._check_view(file, 'admin'))
        self.assertTrue(self._check_view(file, 'editor'))
        self.assertTrue(self._check_view(file, 'reader'))
        self.assertFalse(self._check_view(file, None))

    def test_image_edit_permission_published(self):
        portal = self.layer['portal']
        image_id = portal['test-folder'].invokeFactory('Image', id='image')
        image = portal['test-folder'][image_id]
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(image, 'review_state'),
                         'published')

        self.assertFalse(self._check_edit(image, 'member'))
        self.assertTrue(self._check_edit(image, 'admin'))
        self.assertTrue(self._check_edit(image, 'editor'))
        self.assertFalse(self._check_edit(image, 'reader'))
        self.assertFalse(self._check_edit(image, None))

    def test_image_view_permission_published(self):
        portal = self.layer['portal']
        image_id = portal['test-folder'].invokeFactory('Image', id='image')
        image = portal['test-folder'][image_id]
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(image, 'review_state'),
                         'published')

        self.assertTrue(self._check_view(image, 'member'))
        self.assertTrue(self._check_view(image, 'admin'))
        self.assertTrue(self._check_view(image, 'editor'))
        self.assertTrue(self._check_view(image, 'reader'))
        self.assertFalse(self._check_view(image, None))
