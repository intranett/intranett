from zope.component import getSiteManager, getUtility
from plone.portlets.interfaces import IPortletManager
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
            
    def test_frontpge_view_registration(self):
        self.assert_('frontpage_view' in [v[0] for v in self.portal.getAvailableLayouts()], 'frontpage_view is not registered for Plone Site')
        
    def test_frontpage_view_is_default(self):
        self.assertEquals(self.portal.getLayout(), 'frontpage_view', 'frontpage_view is not default view for Plone Site')
    
    def test_portletmanagers_registration(self):
        sm = getSiteManager(self.portal)
        registrations = [r.name for r in sm.registeredUtilities()
                            if IPortletManager == r.provided]
        self.assert_('frontpage.highlight' in registrations, 'frontpage.highlight is not registered')
        self.assert_('frontpage.portlets.left' in registrations, 'frontpage.portlets.left is not registered')
        self.assert_('frontpage.portlets.right' in registrations, 'frontpage.portlets.right is not registered')
        self.assert_('frontpage.bottom' in registrations, 'frontpage.bottom is not registered')
        
    def testFrontpageInterfaces(self):
        highlight = getUtility(IPortletManager, 'frontpage.highlight')
        portlets_right = getUtility(IPortletManager, 'frontpage.portlets.left')
        portlets_left = getUtility(IPortletManager, 'frontpage.portlets.right')
        bottom = getUtility(IPortletManager, 'frontpage.bottom')        

        self.failUnless(IFrontpagePortletManagers.providedBy(highlight))
        self.failUnless(IFrontpagePortletManagers.providedBy(portlets_right))
        self.failUnless(IFrontpagePortletManagers.providedBy(portlets_left))        
        self.failUnless(IFrontpagePortletManagers.providedBy(bottom))                