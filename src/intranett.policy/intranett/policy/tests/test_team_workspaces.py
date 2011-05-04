from zope.lifecycleevent import ObjectCreatedEvent
from Products.CMFCore.utils import getToolByName
import transaction
from zExceptions import Unauthorized
import zope.event

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase

class TestDualWorkflow(IntranettFunctionalTestCase):
    
    def setUp(self):
        portal = self.layer['portal']
        self.folder = portal['test-folder']
        workspace_id = self.folder.invokeFactory('TeamWorkspace', 'workspace')
        self.workspace = self.folder[workspace_id]
        zope.event.notify(ObjectCreatedEvent(self.workspace))
        self.wf = portal.portal_workflow
    
    def test_new_workspace_private_and_protected(self):
        getInfoFor = self.wf.getInfoFor
        
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'private')
        self.assertEqual(getInfoFor(self.workspace, 'workspace_visibility'), 'private')
    
    def test_published_workspace_published_and_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'published')
        self.assertEqual(getInfoFor(self.workspace, 'workspace_visibility'), 'public')
    
    def test_rehidden_workspace_private_and_protected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        self.wf.doActionFor(self.workspace, "hide")
        
        self.assertEqual(getInfoFor(self.workspace, 'review_state'), 'private')
        self.assertEqual(getInfoFor(self.workspace, 'workspace_visibility'), 'private')
        
    def test_existing_content_in_workspace_is_protected_on_hiding(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.wf.doActionFor(self.workspace, "hide")
        
        self.assertEqual(getInfoFor(self.workspace[link_id], 'workspace_visibility'), 'private')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'private')
    
    def test_existing_content_in_workspace_is_unprotected_on_publishing(self):
        getInfoFor = self.wf.getInfoFor
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        self.wf.doActionFor(self.workspace, "publish")
        
        self.assertEqual(getInfoFor(self.workspace[link_id], 'workspace_visibility'), 'public')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'public')
    
    def test_new_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        
        self.assertEqual(getInfoFor(self.workspace[link_id], 'workspace_visibility'), 'private')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'private')
    
    def test_new_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        link_id = self.workspace.invokeFactory("Link", "link")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        
        self.assertEqual(getInfoFor(self.workspace[link_id], 'workspace_visibility'), 'public')
        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'public')
    
    def test_new_content_outside_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        link_id = self.folder.invokeFactory("Link", "link")
        doc_id = self.folder.invokeFactory("Document", "doc")
        
        self.assertEqual(getInfoFor(self.folder[link_id], 'workspace_visibility'), 'public')
        self.assertEqual(getInfoFor(self.folder[doc_id], 'workspace_visibility'), 'public')

    def test_copypasted_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)

        cb = self.folder.manage_copyObjects('doc')
        self.workspace.manage_pasteObjects(cb)

        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'private')
    
    def test_copypasted_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)

        cb = self.folder.manage_copyObjects('doc')
        self.workspace.manage_pasteObjects(cb)        

        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'public')
        
    def test_cutpasted_content_in_private_workspace_is_protected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)

        cb = self.folder.manage_cutObjects('doc')
        self.workspace.manage_pasteObjects(cb)

        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'private')

    def test_cutpasted_content_in_public_workspace_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.folder.invokeFactory("Document", "doc")
        transaction.savepoint(True)

        cb = self.folder.manage_cutObjects('doc')
        self.workspace.manage_pasteObjects(cb)        

        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'public')

    def test_renamed_content_in_private_workspace_remains_protected(self):
        getInfoFor = self.wf.getInfoFor
        self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)

        self.workspace.manage_renameObject('doc', 'doc1')

        self.assertEqual(getInfoFor(self.workspace['doc1'], 'workspace_visibility'), 'private')

    def test_renamed_content_in_public_workspace_remains_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)
        self.workspace.manage_renameObject('doc', 'doc1')
        self.assertEqual(getInfoFor(self.workspace['doc1'], 'workspace_visibility'), 'public')

    def test_content_cutpasted_from_private_workspace_to_outside_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        doc_id = self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)

        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'private')
        cb = self.workspace.manage_cutObjects('doc')
        self.folder.manage_pasteObjects(cb)        
        self.assertEqual(getInfoFor(self.folder[doc_id], 'workspace_visibility'), 'public')

    def test_content_cutpasted_from_public_workspace_to_outside_is_unprotected(self):
        getInfoFor = self.wf.getInfoFor
        self.wf.doActionFor(self.workspace, "publish")
        doc_id = self.workspace.invokeFactory("Document", "doc")
        transaction.savepoint(True)

        self.assertEqual(getInfoFor(self.workspace[doc_id], 'workspace_visibility'), 'public')
        cb = self.workspace.manage_cutObjects('doc')
        self.folder.manage_pasteObjects(cb)        
        self.assertEqual(getInfoFor(self.folder[doc_id], 'workspace_visibility'), 'public')


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
        zope.event.notify(ObjectCreatedEvent(workspace))
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
        zope.event.notify(ObjectCreatedEvent(workspace))
        wt.doActionFor(workspace, 'publish')
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('member1', 'secret', ['Member'], [])
        transaction.commit()
                
        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.handleErrors = False
        browser.open(workspace.absolute_url()+"/edit")
        browser.getControl(name="members:lines").value = "member1"
        browser.getControl("Lagre").click()
        self.assertIn("member1", workspace.members)
    
    def test_members_shown_on_workspace_home(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')
    
        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        zope.event.notify(ObjectCreatedEvent(workspace))
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
        zope.event.notify(ObjectCreatedEvent(workspace))
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
        zope.event.notify(ObjectCreatedEvent(workspace))
        document_id = workspace.invokeFactory("Document", "qwertyuiop")
        document = workspace[document_id]
        wt.doActionFor(workspace, 'publish')
        wt.doActionFor(document, 'publish')
        
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
        zope.event.notify(ObjectCreatedEvent(workspace))
        
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
            
    def test_publishing_content_in_private_space_doesnt_reveal_it(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')
    
        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        zope.event.notify(ObjectCreatedEvent(workspace))
        document_id = workspace.invokeFactory("Document", "qwertyuiop")
        document = workspace[document_id]
        wt.doActionFor(document, 'publish')
        
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('nonmember', 'secret', ['Member'], [])
        transaction.commit()
                
        browser = get_browser(self.layer['app'], loggedIn=False)
        auth = 'Basic %s:%s' % ('nonmember', 'secret')
        browser.addHeader('Authorization', auth)
        browser.handleErrors = False
        with self.assertRaises(Unauthorized):
            browser.open(document.absolute_url())
    
