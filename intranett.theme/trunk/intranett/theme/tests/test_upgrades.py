from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.upgrades import run_upgrade

THEME_PROFILE = "intranett.theme:default"


class TestFullUpgrade(IntranettTestCase):

    def test_list_steps(self):
        # There should be no upgrade steps from the current version
        portal = self.layer['portal']
        setup = getToolByName(portal, "portal_setup")
        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) == 0)

    def test_do_upgrades(self):
        portal = self.layer['portal']
        setup = getToolByName(portal, "portal_setup")
        setRoles(portal, TEST_USER_ID, ['Manager'])

        setup.setLastVersionForProfile(THEME_PROFILE, '1')
        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) > 0)

        run_upgrade(setup, THEME_PROFILE)

        # And we have reached our current profile version
        current = setup.getVersionForProfile(THEME_PROFILE)
        current = tuple(current.split('.'))
        last = setup.getLastVersionForProfile(THEME_PROFILE)
        self.assertEquals(last, current)

        # There are no more upgrade steps available
        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) == 0)


class TestUpgrades(IntranettTestCase):

    def test_one_to_two(self):
        from ..upgradehandlers import add_media_query_maincss
        portal = self.layer['portal']
        css = getToolByName(portal, 'portal_css')
        main = css.getResource('main.css')
        main.setMedia("screen")
        self.assert_(main.getMedia())
        # Run the step
        add_media_query_maincss(portal)
        main = css.getResource('main.css')
        self.assert_(not main.getMedia())

    def test_two_to_three(self):
        from ..upgradehandlers import add_selectivizr_remove_html5_js
        portal = self.layer['portal']
        js = getToolByName(portal, 'portal_javascripts')
        js.registerScript('html5.js')
        js.unregisterResource('selectivizr.js')
        # Run the step
        add_selectivizr_remove_html5_js(portal)
        ids = js.getResourcesDict().keys()
        self.assert_('html5.js' not in ids)
        self.assert_('selectivizr.js' in ids)

    def test_three_to_four(self):
        from ..upgradehandlers import employees_action_i18n_domain
        portal = self.layer['portal']
        atool = getToolByName(portal, 'portal_actions')
        atool.portal_tabs['employee-listing'].i18n_domain = 'intranett'
        # Run the step
        employees_action_i18n_domain(portal)
        action = atool.portal_tabs['employee-listing']
        self.assertEqual(action.i18n_domain, '')
