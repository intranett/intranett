from Products.CMFCore.utils import getToolByName
import transaction
from zExceptions import Unauthorized
import zope.event

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase


class TestWorkflow(IntranettFunctionalTestCase):

    def setUp(self):
        portal = self.layer['portal']
        self.folder = portal['test-folder']
        workspace_id = self.folder.invokeFactory('TeamWorkspace', 'workspace')
        self.workspace = self.folder[workspace_id]
        self.wf = portal.portal_workflow
        self.catalog = portal.portal_catalog

    def checkCatalog(self, container, id, state):
        # Object should be findable in catalog
        path='/'.join(container.getPhysicalPath())
        brains = self.catalog(path=path, getId=id, review_state=state)
        self.assertEqual(len(brains), 1)
        self.assertEqual(brains[0].getId, id)

    def checkOwner(self, context):
        # Owner role should have permissions
        perms = context.permissionsOfRole('Owner')
        perms = sorted(x['name'] for x in perms if x['selected'])
        expected = ['Access contents information', 'Modify portal content', 'View']
        if getattr(context, 'isPrincipiaFolderish', None):
            expected.insert(1, 'Change portal events')
        self.assertEqual(perms, expected)

    def checkNoOwner(self, context):
        # Owner role should not have permissions
        perms = context.permissionsOfRole('Owner')
        perms = sorted(x['name'] for x in perms if x['selected'])
        self.assertEqual(perms, [])

    def test_new_workspace_is_private(self):
        portal = self.layer['portal']
        getInfoFor = self.wf.getInfoFor
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'private')
        self.checkCatalog(portal, 'workspace', 'private')
        self.checkOwner(self.workspace)

    def test_published_workspace_is_published(self):
        portal = self.layer['portal']
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'published')
        self.checkCatalog(portal, 'workspace', 'published')
        self.checkOwner(self.workspace)

    def test_rehidden_workspace_is_private(self):
        portal = self.layer['portal']
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        self.wf.doActionFor(self.workspace, "hide")
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'private')
        self.checkCatalog(portal, 'workspace', 'private')
        self.checkOwner(self.workspace)

    def test_existing_content_in_workspace_is_protected_on_hiding(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])
        self.wf.doActionFor(self.workspace, "hide")
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'protected')
        self.checkCatalog(self.workspace, link_id, 'protected')
        self.checkCatalog(self.workspace, doc_id, 'protected')
        self.checkCatalog(self.workspace, file_id, 'protected')
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_existing_content_in_workspace_is_unprotected_on_publishing(self):
        getInfoFor = self.wf.getInfoFor
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])
        self.wf.doActionFor(self.workspace, "publish")
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'published')
        self.checkCatalog(self.workspace, link_id, 'published')
        self.checkCatalog(self.workspace, doc_id, 'published')
        self.checkCatalog(self.workspace, file_id, 'published')
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_new_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'protected')
        self.checkCatalog(self.workspace, link_id, 'protected')
        self.checkCatalog(self.workspace, doc_id, 'protected')
        self.checkCatalog(self.workspace, file_id, 'protected')
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_new_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'published')
        self.checkCatalog(self.workspace, link_id, 'published')
        self.checkCatalog(self.workspace, doc_id, 'published')
        self.checkCatalog(self.workspace, file_id, 'published')
        self.checkNoOwner(self.workspace[link_id])
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_copypasted_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.folder.invokeFactory("Document", "doc")
        file_id = self.folder.invokeFactory("File", "file")
        self.checkOwner(self.folder[doc_id])
        self.checkOwner(self.folder[file_id])
        transaction.savepoint(True)
        cb = self.folder.manage_copyObjects(['doc', 'file'])
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'protected')
        self.checkCatalog(self.workspace, doc_id, 'protected')
        self.checkCatalog(self.workspace, file_id, 'protected')
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_copypasted_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.folder.invokeFactory("Document", "doc")
        file_id = self.folder.invokeFactory("File", "file")
        self.checkOwner(self.folder[doc_id])
        self.checkOwner(self.folder[file_id])
        transaction.savepoint(True)
        cb = self.folder.manage_copyObjects(['doc', 'file'])
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'published')
        self.checkCatalog(self.workspace, doc_id, 'published')
        self.checkCatalog(self.workspace, file_id, 'published')
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_cutpasted_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.folder.invokeFactory("Document", "doc")
        file_id = self.folder.invokeFactory("File", "file")
        self.checkOwner(self.folder[doc_id])
        self.checkOwner(self.folder[file_id])
        transaction.savepoint(True)
        cb = self.folder.manage_copyObjects(['doc', 'file'])
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'protected')
        self.checkCatalog(self.workspace, doc_id, 'protected')
        self.checkCatalog(self.workspace, file_id, 'protected')
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_cutpasted_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.folder.invokeFactory("Document", "doc")
        file_id = self.folder.invokeFactory("File", "file")
        self.checkOwner(self.folder[doc_id])
        self.checkOwner(self.folder[file_id])
        transaction.savepoint(True)
        cb = self.folder.manage_copyObjects(['doc', 'file'])
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'published')
        self.checkCatalog(self.workspace, doc_id, 'published')
        self.checkCatalog(self.workspace, file_id, 'published')
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])

    def test_renamed_content_in_private_workspace_remains_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.workspace.invokeFactory("Document", "doc")
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])
        transaction.savepoint(True)
        self.workspace.manage_renameObject(doc_id, 'doc1')
        self.workspace.manage_renameObject(file_id, 'file1')
        self.assertEqual(getInfoFor(self.workspace['doc1'], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace['file1'], 'review_state'), 'protected')
        self.checkCatalog(self.workspace, 'doc1', 'protected')
        self.checkCatalog(self.workspace, 'file1', 'protected')
        self.checkNoOwner(self.workspace['doc1'])
        self.checkNoOwner(self.workspace['file1'])

    def test_renamed_content_in_public_workspace_remains_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[doc_id])
        self.checkNoOwner(self.workspace[file_id])
        transaction.savepoint(True)
        self.workspace.manage_renameObject(doc_id, 'doc1')
        self.workspace.manage_renameObject(file_id, 'file1')
        self.assertEqual(getInfoFor(self.workspace['doc1'], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace['file1'], 'review_state'), 'published')
        self.checkCatalog(self.workspace, 'doc1', 'published')
        self.checkCatalog(self.workspace, 'file1', 'published')
        self.checkNoOwner(self.workspace['doc1'])
        self.checkNoOwner(self.workspace['file1'])

    def test_content_cutpasted_from_private_workspace_to_outside_is_private(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.checkNoOwner(self.workspace[doc_id])
        transaction.savepoint(True)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.checkCatalog(self.workspace, doc_id, 'protected')
        cb = self.workspace.manage_cutObjects(doc_id)
        self.folder.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.folder[doc_id], 'review_state'), 'private')
        self.checkCatalog(self.folder, doc_id, 'private')
        self.checkOwner(self.folder[doc_id])

    def test_content_cutpasted_from_public_workspace_to_outside_is_private(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.checkNoOwner(self.workspace[doc_id])
        transaction.savepoint(True)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.checkCatalog(self.workspace, doc_id, 'published')
        cb = self.workspace.manage_cutObjects(doc_id)
        self.folder.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.folder[doc_id], 'review_state'), 'private')
        self.checkCatalog(self.folder, doc_id, 'private')
        self.checkOwner(self.folder[doc_id])

    def test_file_cutpasted_from_private_workspace_to_outside_is_published(self):
        getInfoFor = self.wf.getInfoFor
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[file_id])
        transaction.savepoint(True)
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'protected')
        self.checkCatalog(self.workspace, file_id, 'protected')
        cb = self.workspace.manage_cutObjects(file_id)
        self.folder.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.folder[file_id], 'review_state'), 'published')
        self.checkCatalog(self.folder, file_id, 'published')
        self.checkOwner(self.folder[file_id])

    def test_file_cutpasted_from_public_workspace_to_outside_is_published(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        file_id = self.workspace.invokeFactory("File", "file")
        self.checkNoOwner(self.workspace[file_id])
        transaction.savepoint(True)
        self.assertEqual(getInfoFor(self.workspace[file_id], 'review_state'), 'published')
        self.checkCatalog(self.workspace, file_id, 'published')
        cb = self.workspace.manage_cutObjects(file_id)
        self.folder.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.folder[file_id], 'review_state'), 'published')
        self.checkCatalog(self.folder, file_id, 'published')
        self.checkOwner(self.folder[file_id])


class TestWorkspaces(IntranettFunctionalTestCase):

    def test_create_workspace(self):
        portal = self.layer['portal']
        folder = portal['test-folder']

        folder.invokeFactory('TeamWorkspace', 'workspace')

    def test_workspace_creator_can_view_workspace(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        wt.doActionFor(workspace, 'publish')
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.open(workspace.absolute_url())

    def test_workspace_creator_can_add_members(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace', title="Workspace", description="ws")
        workspace = folder[workspace_id]
        wt.doActionFor(workspace, 'publish')
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('member1', 'secret', ['Member'], [])
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.handleErrors = False
        browser.open(workspace.absolute_url()+"/edit")
        browser.getControl(name="members:list").value = ["member1"]
        browser.getControl("Lagre").click()
        self.assertIn("member1", workspace.members)

    def test_members_shown_on_workspace_home(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        wt.doActionFor(workspace, 'publish')

        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('member1', 'secret', ['Member'], [])
        portal.portal_membership.getMemberById("member1").setMemberProperties({"fullname": "Max Mustermann", })
        workspace.members = ('member1', )
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.handleErrors = False
        browser.open(workspace.absolute_url())
        self.assertTrue("Max Mustermann" in browser.contents)

    def test_members_can_add_content_in_workspace(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        wt.doActionFor(workspace, 'publish')

        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('member1', 'secret', ['Member'], [])
        workspace.members = ('member1', )
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=False)
        auth = 'Basic %s:%s' % ('member1', 'secret')
        browser.addHeader('Authorization', auth)
        browser.handleErrors = False
        browser.open(workspace.absolute_url())
        browser.getLink(id="document").click()
        browser.getControl(name="title").value="Qwertyuiop"
        browser.getControl(name="text").value="qazxswedc"
        browser.getControl("Lagre").click()

    def test_members_shown_on_subcontent_of_workspace(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        doc_id = workspace.invokeFactory("Document", "contact")
        doc = workspace[doc_id]
        wt.doActionFor(workspace, 'publish')

        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('member1', 'secret', ['Member'], [])
        portal.portal_membership.getMemberById("member1").setMemberProperties({"fullname": "Max Mustermann", })
        workspace.members = ('member1', )
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.handleErrors = False
        browser.open(doc.absolute_url())
        self.assertTrue("Max Mustermann" in browser.contents)

    def test_non_members_can_see_public_workspace_content(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        document_id = workspace.invokeFactory("Document", "qwertyuiop")
        document = workspace[document_id]
        wt.doActionFor(workspace, 'publish')

        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('nonmember', 'secret', ['Member'], [])
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=False)
        auth = 'Basic %s:%s' % ('nonmember', 'secret')
        browser.addHeader('Authorization', auth)
        browser.handleErrors = False
        browser.open(document.absolute_url())

    def test_non_members_cannot_see_private_workspace_in_navigation(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')
        wt.doActionFor(folder, "publish")

        workspace_id = folder.invokeFactory('TeamWorkspace', 'wibblewobblewoo', title="wibblewobblewoo")
        workspace = folder[workspace_id]

        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('nonmember', 'secret', ['Member'], [])
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=False)
        auth = 'Basic %s:%s' % ('nonmember', 'secret')
        browser.addHeader('Authorization', auth)
        browser.handleErrors = False
        browser.open(folder.absolute_url())
        self.assertFalse("wibblewobblewoo" in browser.contents)

        # We then make it public
        wt.doActionFor(workspace, 'publish')
        transaction.commit()

        browser.open(folder.absolute_url())
        self.assertTrue("wibblewobblewoo" in browser.contents)

    def test_owner_of_protected_content_in_workspace_cannot_see_it_when_not_a_member(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        document_id = workspace.invokeFactory("Document", "qwertyuiop")
        document = workspace[document_id]

        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('nonmember', 'secret', ['Member'], [])
        document.manage_setLocalRoles('nonmember', ["Owner"])
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=False)
        auth = 'Basic %s:%s' % ('nonmember', 'secret')
        browser.addHeader('Authorization', auth)
        browser.handleErrors = False
        with self.assertRaises(Unauthorized):
            browser.open(document.absolute_url())

    def test_owner_of_published_content_in_workspace_cannot_edit_it_when_not_a_member(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        document_id = workspace.invokeFactory("Document", "qwertyuiop")
        document = workspace[document_id]
        wt.doActionFor(workspace, 'publish')

        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('nonmember', 'secret', ['Member'], [])
        document.manage_setLocalRoles('nonmember', ["Owner"])
        transaction.commit()

        browser = get_browser(self.layer['app'], loggedIn=False)
        auth = 'Basic %s:%s' % ('nonmember', 'secret')
        browser.addHeader('Authorization', auth)
        browser.handleErrors = False
        with self.assertRaises(Unauthorized):
            browser.open(document.absolute_url()+'/edit')

