import os.path

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy import tests
from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.utils import makeFileUpload


test_dir = os.path.dirname(tests.__file__)
image_file = os.path.join(test_dir, 'images', 'test.jpg')


class TestEmployeeListing(IntranettTestCase):

    def setUp(self):
        super(TestEmployeeListing, self).setUp()
        membership = self.portal.portal_membership
        default_member = membership.getMemberById(TEST_USER_ID)
        default_member.setMemberProperties(
            dict(fullname='Skip McDonald', email='skip@slaterock.com',
                 position='Manager', department='Rock & Gravel'))
        default_member.changeMemberPortrait(
            makeFileUpload(image_file, 'portrait.jpg', 'image/jpeg'))
        membership.addMember('fred', 'secret', ['Member'], [],
            dict(fullname='Fred Flintstone', email='ff@slaterock.com',
                 position='Crane Operator', department='Rock & Gravel'))
        membership.addMember('barney', 'secret', ['Member'], [],
            dict(fullname='Barney Rubble', email='br@slaterock.com',
                 position='Head Accountant', department='Accounting'))

    def test_view_exists(self):
        try:
            self.portal.unrestrictedTraverse('@@employee-listing')
        except AttributeError: # pragma: no cover
            self.fail("@@employee-listing doesn't exist.")

    def test_employeelisting_action(self):
        at = getToolByName(self.portal, 'portal_actions')
        tabs = at.portal_tabs
        self.assert_('employee-listing' in tabs.objectIds(),
                     '"employee-listing" action is not registered.')

    def test_list_employees(self):
        view = self.portal.unrestrictedTraverse('@@employee-listing')
        view.update()
        self.assertEqual([x['fullname'] for x in view.employees()],
                         ['Barney Rubble', 'Fred Flintstone', 'Skip McDonald'])

    def test_list_departments(self):
        view = self.portal.unrestrictedTraverse('@@employee-listing')
        view.update()
        self.assertEqual(view.departments(), ['Accounting', 'Rock & Gravel'])

    def test_list_employees_by_department(self):
        view = self.portal.unrestrictedTraverse('@@employee-listing')
        view.update()
        rocks = [x['fullname'] for x in view.employees('Rock & Gravel')]
        self.assertEqual(rocks, ['Fred Flintstone', 'Skip McDonald'])
        accounting = [x['fullname'] for x in view.employees('Accounting')]
        self.assertEqual(accounting, ['Barney Rubble'])

    def test_can_manage(self):
        view = self.portal.unrestrictedTraverse('@@employee-listing')
        self.assertFalse(view.can_manage())
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.assertTrue(view.can_manage())


class TestFunctionalEmployeeListing(IntranettFunctionalTestCase):

    def test_employee_listing_view(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        mtool = getToolByName(portal, 'portal_membership')

        # Add some users
        for i in range(1, 4):
            mid = 'member-%d' % i
            mtool.addMember(mid, 'secret', ['Member'], [])
            member = mtool.getMemberById(mid)
            email = 'ff%d@slaterock.com' % i
            fullname='Memb\xc3\xa5r %d' % i
            member.setMemberProperties(dict(fullname=fullname,
                                           email=email,
                                           position='Crane Operator',
                                           department='Dept\xc3\xa5 1'))

        # Set a user to a different department
        member = mtool.getMemberById('member-3')
        member.setMemberProperties(dict(department='Dept\xc3\xa5 2'))

        # As a normal user we can view the listing
        browser = get_browser(self.layer)
        browser.open('http://nohost/plone/employee-listing')
        self.assert_(browser.url.endswith('employee-listing'))
