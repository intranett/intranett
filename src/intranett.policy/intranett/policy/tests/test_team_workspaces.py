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

    def checkCatalog(self, id, state):
        brains = self.catalog(getId=id, review_state=state)
        self.assertEqual(len(brains), 1)
        self.assertEqual(brains[0].getId, id)

    def test_new_workspace_is_private(self):
        getInfoFor = self.wf.getInfoFor
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'private')
        self.checkCatalog('workspace', 'private')

    def test_published_workspace_is_published(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'published')
        self.checkCatalog('workspace', 'published')

    def test_rehidden_workspace_is_private(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        self.wf.doActionFor(self.workspace, "hide")
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'private')
        self.checkCatalog('workspace', 'private')

    def test_existing_content_in_workspace_is_protected_on_hiding(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.wf.doActionFor(self.workspace, "hide")
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.checkCatalog(link_id, 'protected')
        self.checkCatalog(doc_id, 'protected')

    def test_existing_content_in_workspace_is_unprotected_on_publishing(self):
        getInfoFor = self.wf.getInfoFor
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.wf.doActionFor(self.workspace, "publish")
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.checkCatalog(link_id, 'published')
        self.checkCatalog(doc_id, 'published')

    def test_new_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'protected')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.checkCatalog(link_id, 'protected')
        self.checkCatalog(doc_id, 'protected')

    def test_new_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.assertEqual(getInfoFor(self.workspace[link_id], 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.checkCatalog(link_id, 'published')
        self.checkCatalog(doc_id, 'published')

#    def test_new_content_outside_workspace_is_unprotected(self):
#        getInfoFor = self.wf.getInfoFor
#        link_id = self.folder.invokeFactory("Link", "link")
#        doc_id = self.folder.invokeFactory("Document", "doc")
#
#        self.assertEqual(getInfoFor(self.folder[link_id], 'workspace_visibility'), 'public')
#        self.assertEqual(getInfoFor(self.folder[doc_id], 'workspace_visibility'), 'public')
#
    def test_copypasted_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        cb = self.folder.manage_copyObjects('doc')
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.checkCatalog(doc_id, 'protected')

    def test_copypasted_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        cb = self.folder.manage_copyObjects('doc')
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.checkCatalog(doc_id, 'published')

    def test_cutpasted_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        cb = self.folder.manage_cutObjects('doc')
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.checkCatalog(doc_id, 'protected')

    def test_cutpasted_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        cb = self.folder.manage_cutObjects('doc')
        self.workspace.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.checkCatalog(doc_id, 'published')

    def test_renamed_content_in_private_workspace_remains_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        self.workspace.manage_renameObject('doc', 'doc1')
        self.assertEqual(getInfoFor(self.workspace['doc1'], 'review_state'), 'protected')
        self.checkCatalog('doc1', 'protected')

    def test_renamed_content_in_public_workspace_remains_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        self.workspace.manage_renameObject('doc', 'doc1')
        self.assertEqual(getInfoFor(self.workspace['doc1'], 'review_state'), 'published')
        self.checkCatalog('doc1', 'published')

    def test_content_cutpasted_from_private_workspace_to_outside_is_private(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'protected')
        self.checkCatalog(doc_id, 'protected')
        cb = self.workspace.manage_cutObjects('doc')
        self.folder.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.folder[doc_id], 'review_state'), 'private')
        self.checkCatalog(doc_id, 'private')

    def test_content_cutpasted_from_public_workspace_to_outside_is_private(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'review_state'), 'published')
        self.checkCatalog(doc_id, 'published')
        cb = self.workspace.manage_cutObjects('doc')
        self.folder.manage_pasteObjects(cb)
        self.assertEqual(getInfoFor(self.folder[doc_id], 'review_state'), 'private')
        self.checkCatalog(doc_id, 'private')


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

