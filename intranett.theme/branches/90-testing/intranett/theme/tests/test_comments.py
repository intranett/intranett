import unittest2 as unittest

from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
import transaction

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase


class TestComments(IntranettFunctionalTestCase):

    @unittest.expectedFailure
    def test_add_comment(self):
        portal = self.layer['portal']
        folder = portal['test-folder']

        folder.invokeFactory('Document', 'doc1')
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(folder.doc1, 'publish')

        addUser = aq_get(portal, 'acl_users').userFolderAddUser
        addUser('member', 'secret', ['Member', 'Reader'], [])

        mtool = getToolByName(portal, 'portal_membership')
        mdata = mtool.getMemberById('member')
        mdata.setMemberProperties(dict(fullname='M\xc3\xa5mb\xc3\xb8r'))

        # XXX This breaks isolation
        # transaction.commit()

        # Get us a test browser with our new user
        browser = get_browser(self.layer, loggedIn=False)
        browser.addHeader('Authorization', 'Basic member:secret')

        browser.open(folder.doc1.absolute_url())
        self.assertEquals(browser.url, 'http://nohost/plone/test-folder/doc1')

        # Fill in a comment
        text = browser.getControl(name='form.widgets.text')
        text.value = 'T\xc3\xa5st http://intranett.no'

        browser.getControl(name='form.buttons.comment').click()

        # The comment was added
        self.assert_('<a href="http://nohost/plone/author/member">'
                     'M\xc3\xa5mb\xc3\xb8r</a>' in browser.contents)

        # The link turned into a proper clickable one
        self.assert_('T&aring;st <a href="http://intranett.no" rel="nofollow">'
                     'http://intranett.no</a>' in browser.contents)
