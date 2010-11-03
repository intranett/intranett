from plone.portlets.interfaces import IPortletManager
import transaction
from zope.component import getSiteManager
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.base import IntranettTestCase
from intranett.theme.browser.interfaces import IFrontpagePortletManagers


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
        portal = self.layer['portal']
        mapping = portal.restrictedTraverse(highlight)
        self.assert_(u'highlight' in mapping.keys(),
                     'Highlight static portlet is not registered for '
                     'frontpage.highlight')

    def test_static_portlet_in_bottom(self):
        bottom = '++contextportlets++frontpage.bottom'
        portal = self.layer['portal']
        mapping = portal.restrictedTraverse(bottom)
        self.assert_(u'bottom' in mapping.keys(),
                     'Bottom static portlet is not registered for '
                     'frontpage.bottom')

    def test_news_in_frontpage_left(self):
        portlets_left = '++contextportlets++frontpage.portlets.left'
        portal = self.layer['portal']
        mapping = portal.restrictedTraverse(portlets_left)
        self.assert_(u'news' in mapping.keys(),
                     'News portlet is not registered for portlets.left')

    def test_events_in_frontpage_central(self):
        portlets_central = '++contextportlets++frontpage.portlets.central'
        portal = self.layer['portal']
        mapping = portal.restrictedTraverse(portlets_central)
        self.assert_(u'events' in mapping.keys(),
                     'Events portlet is not registered for portlets.central')

    def test_static_in_frontpage_right(self):
        portlets_right = '++contextportlets++frontpage.portlets.right'
        portal = self.layer['portal']
        mapping = portal.restrictedTraverse(portlets_right)
        self.assert_(u'fp_static_right' in mapping.keys(),
                     'FP static right is not registered for portlets.right')

    def test_columns_class_default(self):
        portal = self.layer['portal']
        view = portal.unrestrictedTraverse('@@frontpage_view')
        self.assertEquals(view.columns_class(), 'width-16')

    def test_columns_class_no_portlets(self):
        sm = getSiteManager()
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.left')
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.central')
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.right')

        portal = self.layer['portal']
        view = portal.unrestrictedTraverse('@@frontpage_view')
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

    def test_two_columns(self):
        portal = self.layer['portal']
        folder = portal['test-folder']

        # Add a News Item to show on the frontpage
        folder.invokeFactory('News Item', id='n1', title='Test News Item')
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.doActionFor(folder.n1, 'publish')

        transaction.commit()

        browser = get_browser(self.layer)
        browser.open(portal.absolute_url())

        self.assert_('Test News Item' in browser.contents)
        self.assert_('"cell fpBlock width-8"' in browser.contents)

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

        transaction.commit()

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
