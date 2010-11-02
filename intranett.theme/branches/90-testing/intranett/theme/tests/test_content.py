import os.path
import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.portlets.interfaces import IPortletManager
from zope.component import getSiteManager, getUtility
from Products.CMFCore.utils import getToolByName

from intranett.policy import tests
from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.utils import makeFileUpload
from intranett.theme.browser.interfaces import IFrontpagePortletManagers


test_dir = os.path.dirname(tests.__file__)
image_file = os.path.join(test_dir, 'images', 'test.jpg')


class TestContent(IntranettTestCase):

    def test_navigation_portlet(self):
        leftcolumn = '++contextportlets++plone.leftcolumn'
        mapping = self.portal.restrictedTraverse(leftcolumn)
        self.assert_(u'navigation' in mapping.keys())
        nav = mapping[u'navigation']
        self.assertEquals(nav.topLevel, 1)
        self.assertEquals(nav.currentFolderOnly, True)


class TestFrontpage(IntranettTestCase):

    def test_frontpage_view_registration(self):
        layouts = [v[0] for v in self.portal.getAvailableLayouts()]
        self.assert_('frontpage_view' in layouts,
                     'frontpage_view is not registered for Plone Site')

    def test_frontpage_view_is_default(self):
        self.assertEquals(self.portal.getLayout(), 'frontpage_view',
                          'frontpage_view is not default view for Plone Site')

    def test_portletmanagers_registration(self):
        sm = getSiteManager(self.portal)
        registrations = [r.name for r in sm.registeredUtilities()
                         if IPortletManager == r.provided]
        self.assert_('frontpage.highlight' in registrations)
        self.assert_('frontpage.portlets.left' in registrations)
        self.assert_('frontpage.portlets.central' in registrations)
        self.assert_('frontpage.portlets.right' in registrations)
        self.assert_('frontpage.bottom' in registrations)

    def testFrontpageInterfaces(self):
        highlight = getUtility(IPortletManager, 'frontpage.highlight')
        portlets_right = getUtility(IPortletManager,
                                    'frontpage.portlets.right')
        portlets_central = getUtility(IPortletManager,
                                      'frontpage.portlets.central')
        portlets_left = getUtility(IPortletManager, 'frontpage.portlets.left')
        bottom = getUtility(IPortletManager, 'frontpage.bottom')

        self.failUnless(IFrontpagePortletManagers.providedBy(highlight))
        self.failUnless(IFrontpagePortletManagers.providedBy(portlets_right))
        self.failUnless(IFrontpagePortletManagers.providedBy(portlets_central))
        self.failUnless(IFrontpagePortletManagers.providedBy(portlets_left))
        self.failUnless(IFrontpagePortletManagers.providedBy(bottom))

    def test_static_portlet_in_highlight(self):
        highlight = '++contextportlets++frontpage.highlight'
        mapping = self.portal.restrictedTraverse(highlight)
        self.assert_(u'highlight' in mapping.keys(),
                     'Highlight static portlet is not registered for '
                     'frontpage.highlight')

    def test_static_portlet_in_bottom(self):
        bottom = '++contextportlets++frontpage.bottom'
        mapping = self.portal.restrictedTraverse(bottom)
        self.assert_(u'bottom' in mapping.keys(),
                     'Bottom static portlet is not registered for '
                     'frontpage.bottom')

    def test_news_in_frontpage_left(self):
        portlets_left = '++contextportlets++frontpage.portlets.left'
        mapping = self.portal.restrictedTraverse(portlets_left)
        self.assert_(u'news' in mapping.keys(),
                     'News portlet is not registered for portlets.left')

    def test_events_in_frontpage_central(self):
        portlets_central = '++contextportlets++frontpage.portlets.central'
        mapping = self.portal.restrictedTraverse(portlets_central)
        self.assert_(u'events' in mapping.keys(),
                     'Events portlet is not registered for portlets.central')

    def test_static_in_frontpage_right(self):
        portlets_right = '++contextportlets++frontpage.portlets.right'
        mapping = self.portal.restrictedTraverse(portlets_right)
        self.assert_(u'fp_static_right' in mapping.keys(),
                     'FP static right is not registered for portlets.right')

    def test_columns_class_default(self):
        view = self.portal.unrestrictedTraverse('@@frontpage_view')
        self.assertEquals(view.columns_class(), 'width-16')

    def test_columns_class_no_portlets(self):
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.left')
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.central')
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.right')

        view = self.portal.unrestrictedTraverse('@@frontpage_view')
        self.assertEquals(view.columns_class(), False)


class TestFunctionalFrontpage(IntranettFunctionalTestCase):

    def test_anon_frontpage(self):
        portal = self.layer['portal']
        browser = get_browser(self.layer, loggedIn=False)

        # Navigating to the front page redirects us to the login form
        browser.open(portal.absolute_url())
        self.assert_('require_login' in browser.url)
        self.assert_('template-login_form' in browser.contents)
        self.assert_('id="login_form"' in browser.contents)

    def test_one_column(self):
        portal = self.layer['portal']
        browser = get_browser(self.layer)
        browser.open(portal.absolute_url())
        self.assertEquals(browser.url, 'http://nohost/plone')

        # The frontpage view is the default view of the site
        self.assert_('template-frontpage_view' in browser.contents)

        # By default we should have only one content column on the frontpage,
        # which has a static portlet with dummy content assigned to it. The two
        # other columns should have nothing and should not be rendered since
        # we have no news or events published yet. In this case we should get
        # full-width CSS class from our view
        self.assert_('class="cell fpBlock width-16"' in browser.contents)

    @unittest.expectedFailure
    def test_two_columns(self):
        portal = self.layer['portal']
        folder = portal['test-folder']

        # Add a News Item to show on the frontpage
        folder.invokeFactory('News Item', id='n1', title='Test News Item')
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(folder.n1, 'publish')

        browser = get_browser(self.layer)
        browser.open(portal.absolute_url())

        self.assert_('Test News Item' in browser.contents)
        self.assert_('"cell fpBlock width-8"' in browser.contents)

    @unittest.expectedFailure
    def test_three_columns(self):
        portal = self.layer['portal']
        folder = portal['test-folder']

        # Add a News Item and Event to show on the frontpage
        folder.invokeFactory('News Item', id='n1', title='Test News Item')
        folder.invokeFactory('Event', id='e1', title='Test Event',
                             start_date='2011-01-01', end_date='2100-01-01')

        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(folder.n1, 'publish')
        wftool.doActionFor(folder.e1, 'publish')

        browser = get_browser(self.layer)
        browser.open(portal.absolute_url())

        self.assert_('Test News Item' in browser.contents)
        self.assert_('Test Event' in browser.contents)
        self.assert_('"cell fpBlock width-5"' in browser.contents)

    def test_manage_frontpage(self):
        # Let's make sure we have edit-bar when we edit the frontpage
        browser = get_browser(self.layer)
        browser.open('http://nohost/plone/@@manage-frontpage')
        self.assert_('<ul class="contentViews" id="content-views">'
                     in browser.contents)


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
        self.login(TEST_USER_NAME)
        self.assertFalse(view.can_manage())
        self.loginAsPortalOwner()
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
