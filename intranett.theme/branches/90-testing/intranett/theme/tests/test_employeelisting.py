import os.path
import unittest2 as unittest

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy import tests
from intranett.policy.tests.base import get_browser
from intranett.policy.tests.layer import FunctionalTesting
from intranett.policy.tests.layer import IntegrationTesting
from intranett.policy.tests.layer import INTRANETT_LAYER
from intranett.policy.tests.utils import make_file_upload


test_dir = os.path.dirname(tests.__file__)
image_file = os.path.join(test_dir, 'images', 'test.jpg')


class EmployeeListingLayer(PloneSandboxLayer):

    defaultBases = (INTRANETT_LAYER,)

    def setUpPloneSite(self, portal):
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


EMPLOYEE_LISTING_LAYER = EmployeeListingLayer()
EMPLOYEE_LISTING_INTEGRATION = IntegrationTesting(
    bases=(EMPLOYEE_LISTING_LAYER,), name="EmployeeListingLayer:Integration")
EMPLOYEE_LISTING_FUNCTIONAL = FunctionalTesting(
    bases=(EMPLOYEE_LISTING_LAYER,), name="EmployeeListingLayer:Functional")


class TestEmployeeListing(unittest.TestCase):

    layer = EMPLOYEE_LISTING_INTEGRATION

    def test_view_exists(self):
        portal = self.layer['portal']
        try:
            portal.unrestrictedTraverse('@@employee-listing')
        except AttributeError: # pragma: no cover
            self.fail("@@employee-listing doesn't exist.")

    def test_employeelisting_action(self):
        portal = self.layer['portal']
        at = getToolByName(portal, 'portal_actions')
        tabs = at.portal_tabs
        self.assert_('employee-listing' in tabs.objectIds(),
                     '"employee-listing" action is not registered.')

    def test_list_employees(self):
        portal = self.layer['portal']
        view = portal.unrestrictedTraverse('@@employee-listing')
        view.update()
        self.assertEqual([x['fullname'] for x in view.employees()],
                         ['Barney Rubble', 'Fred Flintstone', 'Memb\xc3\xa5r'])

    def test_list_departments(self):
        portal = self.layer['portal']
        view = portal.unrestrictedTraverse('@@employee-listing')
        view.update()
        self.assertEqual(view.departments(), ['Dept\xc3\xa5', 'Rock & Gravel'])

    def test_list_employees_by_department(self):
        portal = self.layer['portal']
        view = portal.unrestrictedTraverse('@@employee-listing')
        view.update()
        rocks = [x['fullname'] for x in view.employees('Rock & Gravel')]
        self.assertEqual(rocks, ['Fred Flintstone', 'Memb\xc3\xa5r'])
        accounting = [x['fullname'] for x in view.employees('Dept\xc3\xa5')]
        self.assertEqual(accounting, ['Barney Rubble'])

    def test_can_manage(self):
        portal = self.layer['portal']
        view = portal.unrestrictedTraverse('@@employee-listing')
        self.assertFalse(view.can_manage())
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.assertTrue(view.can_manage())


class TestFunctionalEmployeeListing(unittest.TestCase):

    layer = EMPLOYEE_LISTING_FUNCTIONAL

    def test_employee_listing_view(self):
        # As a normal user we can view the listing
        browser = get_browser(self.layer['app'])
        browser.open('http://nohost/plone/employee-listing')
        self.assert_(browser.url.endswith('employee-listing'))
