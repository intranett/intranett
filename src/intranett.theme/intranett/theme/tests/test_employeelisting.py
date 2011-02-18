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


class TestEmployeeListing(IntranettTestCase):

    def setUp(self):
        super(TestEmployeeListing, self).setUp()
        portal = self.layer['portal']
        add_default_members(portal)

    def test_view_exists(self):
        portal = self.layer['portal']
        members = portal['people']
        try:
            members.unrestrictedTraverse('@@employee-listing')
        except AttributeError: # pragma: no cover
            self.fail("@@employee-listing doesn't exist.")

    def test_employeelisting_action(self):
        portal = self.layer['portal']
        atool = getToolByName(portal, 'portal_actions')
        # There is no action anymore
        self.failIf('employee-listing' in atool.portal_tabs.objectIds())

    def test_list_employees(self):
        portal = self.layer['portal']
        members = portal['people']
        view = members.unrestrictedTraverse('@@employee-listing')
        view.update()
        self.assertEqual([x['fullname'] for x in view.employees()],
                         ['Barney Rubble', 'Fred Flintstone', 'Memb\xc3\xa5r'])

    def test_list_departments(self):
        portal = self.layer['portal']
        members = portal['people']
        view = members.unrestrictedTraverse('@@employee-listing')
        view.update()
        self.assertEqual([x['name'] for x in view.departments()],
                         ['Dept\xc3\xa5', 'Rock & Gravel'])

    def test_list_employees_by_department(self):
        portal = self.layer['portal']
        members = portal['people']
        view = members.unrestrictedTraverse('@@employee-listing')
        view.update()
        rocks = [x['fullname'] for x in view.employees('Rock & Gravel')]
        self.assertEqual(rocks, ['Fred Flintstone', 'Memb\xc3\xa5r'])
        accounting = [x['fullname'] for x in view.employees('Dept\xc3\xa5')]
        self.assertEqual(accounting, ['Barney Rubble'])

    def test_can_manage(self):
        portal = self.layer['portal']
        members = portal['people']
        view = members.unrestrictedTraverse('@@employee-listing')
        self.assertFalse(view.can_manage())
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.assertTrue(view.can_manage())


class TestFunctionalEmployeeListing(IntranettFunctionalTestCase):

    def setUp(self):
        super(TestFunctionalEmployeeListing, self).setUp()
        portal = self.layer['portal']
        add_default_members(portal)
        transaction.commit()

    def test_employee_listing_view(self):
        # As a normal user we can view the listing
        browser = get_browser(self.layer['app'])
        browser.open('http://nohost/plone/people/employee-listing')
        self.assert_(browser.url.endswith('employee-listing'))
        self.failUnless('Barney Rubble' in browser.contents)
        self.failUnless('http://nohost/plone/people/barney' in browser.contents)
        self.failUnless('Fred Flintstone' in browser.contents)
        self.failUnless('http://nohost/plone/people/fred' in browser.contents)

    def test_members_folder_view(self):
        # As a normal user we can view the listing
        browser = get_browser(self.layer['app'])
        browser.open('http://nohost/plone/people')
        self.assert_(browser.url.endswith('people'))
        self.failUnless('Barney Rubble' in browser.contents)
        self.failUnless('http://nohost/plone/people/barney' in browser.contents)
        self.failUnless('Fred Flintstone' in browser.contents)
        self.failUnless('http://nohost/plone/people/fred' in browser.contents)

