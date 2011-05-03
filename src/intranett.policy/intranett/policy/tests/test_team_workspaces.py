from Products.CMFCore.utils import getToolByName
import transaction
from zExceptions import Unauthorized

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase

class TestDualWorkflow(IntranettFunctionalTestCase):
    
    def test_new_workspace_private_and_protected(self):
        NotImplemented
    
    def test_published_workspace_published_and_unprotected(self):
        NotImplemented
    
    def test_rehidden_workspace_private_and_protected(self):
        NotImplemented

    def test_existing_content_in_workspace_is_protected_on_hiding(self):
        NotImplemented
    
    def test_existing_content_in_workspace_is_unprotected_on_publishing(self):
        NotImplemented
    
    def test_new_content_in_private_workspace_is_protected(self):
        NotImplemented
    
    def test_new_content_in_public_workspace_is_unprotected(self):
        NotImplemented
    
    def test_new_content_outside_workspace_is_unprotected(self):
        NotImplemented
    

class TestWorkspaces(IntranettFunctionalTestCase):

    def test_create_workspace(self):
        portal = self.layer['portal']
        folder = portal['test-folder']

        folder.invokeFactory('TeamWorkspace', 'workspace')

    def test_workspace_owner_can_view_workspace(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')

        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
        wt.doActionFor(workspace, 'publish')
        transaction.commit()
                
        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.open(workspace.absolute_url())
    
    def test_workspace_owner_can_add_members(self):
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
        browser.getControl(name="members:lines").value = "member1"
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
        workspace.members = ('member1', )
        transaction.commit()
                
        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.handleErrors = False
        browser.open(workspace.absolute_url())
        self.assertTrue("member1" in browser.contents)

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
        NotImplemented
    
    def test_non_members_can_see_public_workspace_content(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')
    
        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
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
    
        workspace_id = folder.invokeFactory('TeamWorkspace', 'wibblewobblewoo', title="wibblewobblewoo")
        workspace = folder[workspace_id]
        
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('nonmember', 'secret', ['Member'], [])
        transaction.commit()
                
        browser = get_browser(self.layer['app'], loggedIn=False)
        auth = 'Basic %s:%s' % ('nonmember', 'secret')
        browser.addHeader('Authorization', auth)
        browser.handleErrors = False
        browser.open(portal.absolute_url())
        self.assertFalse("wibblewobblewoo" in browser.contents)
        
        # We then make it public
        wt.doActionFor(workspace, 'publish')
        transaction.commit()
        
        browser.open(portal.absolute_url())
        self.assertTrue("wibblewobblewoo" in browser.contents)
        
    
    def test_non_members_cannot_see_private_workspace_content(self):
        portal = self.layer['portal']
        folder = portal['test-folder']
        wt = getToolByName(portal, 'portal_workflow')
    
        workspace_id = folder.invokeFactory('TeamWorkspace', 'workspace')
        workspace = folder[workspace_id]
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
            import pdb; pdb.set_trace( )
            browser.open(document.absolute_url())
        
    def test_publishing_content_in_private_space_doesnt_reveal_it(self):
        NotImplemented
    
