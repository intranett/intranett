from Acquisition import aq_get
from Acquisition import aq_parent
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from Products.CMFCore.utils import getToolByName

from intranett.policy.upgrades.tests.base import FunctionalUpgradeTestCase
from intranett.policy.upgrades.tests.utils import ensure_no_addon_upgrades


class TestFunctionalMigrations(FunctionalUpgradeTestCase):

    def test_gs_diff(self):
        self.importFile(__file__, 'one.zexp')
        oldsite, result = self.migrate()

        login(aq_parent(oldsite), SITE_OWNER_NAME)
        diff = self.export()
        remaining = self.parse_diff(diff)

        self.assertEquals(set(remaining.keys()), set([]),
                          "Unexpected diffs in:\n %s" % remaining.items())

    def test_list_steps_for_addons(self):
        self.importFile(__file__, 'one.zexp')
        oldsite, result = self.migrate()

        setup = getToolByName(oldsite, "portal_setup")
        upgrades = ensure_no_addon_upgrades(setup)
        for profile, steps in upgrades.items():
            self.assertEquals(len(steps), 0,
                              "Found unexpected upgrades: %s" % steps)

    def test_one_to_two(self):
        from intranett.policy.setuphandlers import enable_secure_cookies
        portal = self.layer['portal']
        acl = aq_get(portal, 'acl_users')
        acl.session._updateProperty('secure', False)
        # Run the step
        enable_secure_cookies(portal)
        self.assertEqual(acl.session.getProperty('secure'), True)
