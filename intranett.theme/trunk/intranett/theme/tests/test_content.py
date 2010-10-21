from zope.component import getSiteManager, getUtility
from plone.portlets.interfaces import IPortletManager
from Products.CMFCore.utils import getToolByName

from intranett.theme.browser.interfaces import IFrontpagePortletManagers
from intranett.policy.tests.base import IntranettTestCase

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
        portlets_right = getUtility(IPortletManager, 'frontpage.portlets.right')
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

class TestEmployeeListing(IntranettTestCase):

    def test_view_exists(self):
        try:
            self.portal.unrestrictedTraverse('@@employee-listing')
        except AttributeError: # pragma: no cover
            self.fail("@@employee-listing doesn't exist.")

    def test_employeelisting_action(self):
        at = getToolByName(self.portal, 'portal_actions')
        tabs = at.portal_tabs
        self.assert_('employee-listing' in tabs.objectIds(), '"employee-listing" action is not registered.')

