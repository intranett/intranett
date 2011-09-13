from AccessControl import getSecurityManager
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletManager
import transaction
from zope.component import getSiteManager

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.base import IntranettTestCase


class TestFrontpage(IntranettTestCase):

    def test_frontpage_view_registration(self):
        portal = self.layer['portal']
        layouts = [v[0] for v in portal.getAvailableLayouts()]
        self.assert_('frontpage_view' in layouts,
                     'frontpage_view is not registered for Plone Site')

    def test_frontpage_view_is_default(self):
        portal = self.layer['portal']
        self.assertEquals(portal.getLayout(), 'frontpage_view',
                          'frontpage_view is not default view for Plone Site')

    def test_portletmanagers_registration(self):
        sm = getSiteManager()
        registrations = [r.name for r in sm.registeredUtilities()
                         if IPortletManager == r.provided]
        self.assert_('frontpage.main.top' in registrations)
        self.assert_('frontpage.main.left' in registrations)
        self.assert_('frontpage.main.right' in registrations)
        self.assert_('frontpage.main.bottom' in registrations)
        self.assert_('frontpage.portlets.right' in registrations)


class TestFunctionalFrontpage(IntranettFunctionalTestCase):

    def test_anon_frontpage(self):
        portal = self.layer['portal']
        browser = get_browser(self.layer['app'], loggedIn=False)

        # Navigating to the front page redirects us to the login form
        browser.open(portal.absolute_url())
        self.assert_('require_login' in browser.url)
        self.assert_('template-login_form' in browser.contents)
        self.assert_('id="login_form"' in browser.contents)

    def test_personal_frontpage(self):
        # As a normal user, I should be able to assign personal portraits
        portal = self.layer['portal']

        sm = getSecurityManager()
        self.assertEqual(sm.getUser().getId(), TEST_USER_ID)
        self.assertTrue(sm.checkPermission(
            'Portlets: Manage own portlets', portal))

        browser = get_browser(self.layer['app'])
        browser.handleErrors = False
        browser.open('http://nohost/plone/@@manage-dashboard')
        self.assertTrue('+/plone.portlet.static.Static' in browser.contents)
        self.assertTrue('+/portlets.News' in browser.contents)

    def test_edit_frontpage(self):
        # As a Site Administrator we should be able to edit the frontpage
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Member', 'Site Administrator'])
        transaction.commit()

        sm = getSecurityManager()
        self.assertEqual(sm.getUser().getId(), TEST_USER_ID)
        self.assertTrue(sm.checkPermission('Portlets: Manage portlets', portal))

        browser = get_browser(self.layer['app'])
        browser.open('http://nohost/plone/')
        edit = browser.getLink('Redig\xc3\xa9r')
        edit.click()
        self.assertTrue(browser.url.endswith('manage-frontpage'))
        self.assert_('<ul class="contentViews"' in browser.contents)
        # and we can add multiple portlet types
        self.assertTrue('+/plone.portlet.static.Static' in browser.contents)
        self.assertTrue('+/portlets.News' in browser.contents)
