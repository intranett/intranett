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

    def test_js_enabled(self):
        js = getToolByName(self.portal, 'portal_javascripts')
        ids = js.getResourcesDict().keys()
        self.assert_('modernizr.js' in ids)
        self.assert_('jquery.easing.js' in ids)
        self.assert_('jquery.jBreadCrumb.js' in ids)
        self.assert_('main.js' in ids)

    def test_html5_js(self):
        js = getToolByName(self.portal, 'portal_javascripts')
        ids = js.getResourcesDict().keys()
        self.assert_('html5.js' in ids)
        h5 = js.getResource('html5.js')
        self.assertEquals(h5.getConditionalcomment(), 'lt IE 9')

        positions = {}
        for pos, r in enumerate(js.getResources()):
            positions[r.getId()] = pos

        self.assert_(positions['html5.js'] > positions['jquery.js'])
