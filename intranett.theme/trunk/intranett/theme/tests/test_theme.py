from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestTheme(IntranettTestCase):

    def test_theme(self):
        skins = getToolByName(self.portal, 'portal_skins')
        self.assertEquals(skins.getDefaultSkin(), 'Intranett.no base theme')

    def test_icon_visibility(self):
        pp = getToolByName(self.portal, 'portal_properties')
        sp = pp.site_properties
        self.assertEquals(sp.getProperty('icon_visibility'), 'disabled')

    def test_home_action_invisible(self):
        at = getToolByName(self.portal, 'portal_actions')
        tabs = at.portal_tabs
        id_ = 'index_html'
        self.assertEquals(tabs[id_].visible, False)

    def test_reset_css_first(self):
        css = getToolByName(self.portal, 'portal_css')
        self.assertEquals(css.getResources()[0].getId(), 'reset.css')

    def test_css_enabled(self):
        css = getToolByName(self.portal, 'portal_css')
        ids = css.getResourcesDict().keys()
        self.assert_('main.css' in ids)
        self.assert_('decogrids-16.css' in ids)

    def test_css_disabled(self):
        css = getToolByName(self.portal, 'portal_css')
        self.assertEquals(css.getResource('base.css').getEnabled(), False)
        self.assertEquals(css.getResource('portlets.css').getEnabled(), False)
