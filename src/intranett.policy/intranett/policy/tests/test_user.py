# -*- coding: utf-8 -*-
import urllib2
import transaction

from zope.component import queryMultiAdapter
from zope.interface import Interface

from zExceptions import Unauthorized
from Products.CMFCore.utils import getToolByName

from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.base import IntranettFunctionalTestCase


class TestFunctionalUserView(IntranettFunctionalTestCase):

    def test_user_view(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = False
        portal = self.layer['portal']
        browser.open(portal.absolute_url() + '/users')
        self.assertTrue('href="http://nohost/plone/users/test_user_1_"' in
            browser.contents)

    def test_anonymous_user(self):
        browser = get_browser(self.layer['app'], loggedIn=False)
        browser.handleErrors = False
        portal = self.layer['portal']
        try:
            browser.open(portal.absolute_url() + '/users')
        except Unauthorized:
            pass
        else:
            self.fail('Unauthorized not raised') # pragma: no cover

    def test_author_redirects_to_users(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = True
        portal = self.layer['portal']
        browser.open(portal.absolute_url() + '/author')
        self.assertEqual(browser.url, 'http://nohost/plone/users')

    def test_author_userid_redirects_to_users_id(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = True
        portal = self.layer['portal']
        browser.open(portal.absolute_url() + '/author/test_user_1_')
        self.assertEqual(browser.url, 'http://nohost/plone/users/test_user_1_')


class TestPersonalFolders(IntranettTestCase):


    def _createUser(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        mt = getToolByName(portal, 'portal_membership')
        mt.addMember('new_user', 'new_password',
            ['Member'], [])
        setRoles(portal, TEST_USER_ID, ['Member'])

    def test_personal_folder_creation(self):
        self._createUser()
        portal = self.layer['portal']
        login(portal, 'new_user')
        personal = self.layer['portal']['personal']
        self.assertTrue('new_user' in personal)

        # The new user has a personal folder
        folder = personal['new_user']
        self.assertTrue(folder.portal_type, 'Folder')
        # Personal folders are private
        wftool = getToolByName(portal, 'portal_workflow')
        self.assertEqual(wftool.getInfoFor(folder, 'review_state'),
                         'private')
        # New user is the owner of his personal folder
        self.assertEqual(folder.getOwner().getUserId(), 'new_user')
        logout()


    def test_personal_folder_deletion(self):
        self._createUser()
        portal = self.layer['portal']
        personal = portal['personal']
        self.assertTrue('new_user' in personal)

        # Delete the user
        setRoles(portal, TEST_USER_ID, ['Manager'])
        mt = getToolByName(portal, 'portal_membership')
        mt.deleteMembers(['new_user'])
        self.assertTrue('new_user' not in personal)
        setRoles(portal, TEST_USER_ID, ['Member'])


class TestMemberDataView(IntranettTestCase):

    def _make_one(self, request):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        return queryMultiAdapter((member, request), Interface,
            'memberdata_view')

    def test_userid(self):
        request = self.layer['request']
        view = self._make_one(request)
        self.assertEqual(view.userid(), 'test_user_1_')

    def test_username(self):
        request = self.layer['request']
        view = self._make_one(request)
        self.assertEqual(view.username(), 'test-user')

    def test_userinfo(self):
        request = self.layer['request']
        view = self._make_one(request)
        self.assertEqual(view.userinfo()['username'], 'test-user')

    def test_userportrait(self):
        request = self.layer['request']
        view = self._make_one(request)
        portrait = view.userportrait()
        self.assertEqual(portrait.getId(), 'defaultUser.png')
        self.assertEqual(portrait.absolute_url(),
            'http://nohost/plone/defaultUser.png')

    def test_usercontent(self):
        request = self.layer['request']
        view = self._make_one(request)
        self.assertEqual(len(view.usercontent()), 1)
        self.assertEqual(view.usercontent()[0].getId, 'test-folder')

    def test_anonymous_user(self):
        request = self.layer['request']
        logout()
        view = self._make_one(request)
        self.assertEqual(view, None)


class TestFunctionalMemberDataView(IntranettFunctionalTestCase):

    def test_memberdata_view(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = False
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'Bob Døe',
            'email': 'info@jarn.com', 'department': 'it'})
        transaction.commit()
        browser.open(portal.absolute_url() +
            '/users/test_user_1_/memberdata_view')
        self.failUnless('Bob Døe' in browser.contents)
        self.failUnless('info@jarn.com' in browser.contents)

    def test_browser_default(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = False
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties(
            {'fullname': 'Bob Døe', 'email': 'info@jarn.com'})
        transaction.commit()
        browser.open(portal.absolute_url() + '/users/test_user_1_')
        self.failUnless('Bob Døe' in browser.contents)
        self.failUnless('info@jarn.com' in browser.contents)

    def test_unknown_member(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = True
        portal = self.layer['portal']
        try:
            browser.open(portal.absolute_url() + '/users/test_user_2_')
        except urllib2.HTTPError, e:
            self.assertEqual(e.getcode(), 404)
            self.assertEqual('%s' % (e, ), 'HTTP Error 404: Not Found')
        else:
            self.fail('HTTPError not raised') # pragma: no cover

    def test_anonymous_user(self):
        browser = get_browser(self.layer['app'], loggedIn=False)
        browser.handleErrors = False
        portal = self.layer['portal']
        try:
            browser.open(portal.absolute_url() + '/users/test_user_1_')
        except Unauthorized, e:
            self.assertEqual('%s' % (e, ), 'Anonymous rejected')
        else:
            self.fail('Unauthorized not raised') # pragma: no cover
