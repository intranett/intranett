import os.path
import transaction

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy import tests
from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.utils import make_file_upload

test_dir = os.path.dirname(tests.__file__)
image_file = os.path.join(test_dir, 'images', 'test.jpg')


def add_default_members(portal):
    mtool = getToolByName(portal, 'portal_membership')
    default_member = mtool.getMemberById(TEST_USER_ID)
    default_member.setMemberProperties(
        dict(fullname='Memb\xc3\xa5r', email='skip@slaterock.com',
             position='Manager', department='Rock & Gravel'))
    default_member.changeMemberPortrait(
        make_file_upload(image_file, 'portrait.jpg', 'image/jpeg'))
    mtool.addMember('fred', 'secret', ['Member'], [],
        dict(fullname='Fred Flintstone', email='ff@slaterock.com',
             position='Crane Operator', department='Rock & Gravel'))
    mtool.addMember('barney', 'secret', ['Member'], [],
        dict(fullname='Barney Rubble', email='br@slaterock.com',
             position='Head Accountant', department='Dept\xc3\xa5'))


class TestUsersListing(IntranettTestCase):

    def setUp(self):
        super(TestUsersListing, self).setUp()
        portal = self.layer['portal']
        add_default_members(portal)

    def _make_one(self):
        from intranett.policy.config import MEMBERS_FOLDER_ID
        portal = self.layer['portal']
        members = portal[MEMBERS_FOLDER_ID]
        view = members.unrestrictedTraverse('@@users-listing')
        view.update()
        return view

    def test_view_exists(self):
        try:
            self._make_one()
        except AttributeError: # pragma: no cover
            self.assertFalse("@@users-listing doesn't exist.")

    def test_userslisting_action(self):
        portal = self.layer['portal']
        atool = getToolByName(portal, 'portal_actions')
        # There is no action anymore
        self.assertFalse('users-listing' in atool.portal_tabs.objectIds())

    def test_list_users(self):
        view = self._make_one()
        self.assertEqual([x['fullname'] for x in view.users()],
                         ['Barney Rubble', 'Fred Flintstone', 'Memb\xc3\xa5r'])

    def test_list_departments(self):
        view = self._make_one()
        self.assertEqual([x['name'] for x in view.departments()],
                         ['Dept\xc3\xa5', 'Rock & Gravel'])

    def test_list_users_by_department(self):
        view = self._make_one()
        rocks = [x['fullname'] for x in view.users('Rock & Gravel')]
        self.assertEqual(rocks, ['Fred Flintstone', 'Memb\xc3\xa5r'])
        accounting = [x['fullname'] for x in view.users('Dept\xc3\xa5')]
        self.assertEqual(accounting, ['Barney Rubble'])

    def test_can_manage(self):
        portal = self.layer['portal']
        view = self._make_one()
        self.assertFalse(view.can_manage())
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.assertTrue(view.can_manage())


class TestFunctionalUsersListing(IntranettFunctionalTestCase):

    def setUp(self):
        super(TestFunctionalUsersListing, self).setUp()
        portal = self.layer['portal']
        add_default_members(portal)
        transaction.commit()

    def test_users_listing_view(self):
        # As a normal user we can view the listing
        browser = get_browser(self.layer['app'])
        browser.open('http://nohost/plone/users/')
        self.failUnless('Barney Rubble' in browser.contents)
        self.failUnless('http://nohost/plone/users/barney' in browser.contents)
        self.failUnless('Fred Flintstone' in browser.contents)
        self.failUnless('http://nohost/plone/users/fred' in browser.contents)

    def test_members_folder_view(self):
        # As a normal user we can view the listing
        browser = get_browser(self.layer['app'])
        browser.open('http://nohost/plone/users/')
        self.failUnless('Barney Rubble' in browser.contents)
        self.failUnless('http://nohost/plone/users/barney' in browser.contents)
        self.failUnless('Fred Flintstone' in browser.contents)
        self.failUnless('http://nohost/plone/users/fred' in browser.contents)
