from Products.CMFCore.utils import getToolByName

from intranett.policy.config import POLICY_PROFILE
from intranett.policy.config import THEME_PROFILE
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.upgrades import compare_profile_versions
from intranett.policy.upgrades import run_upgrade
from intranett.policy.upgrades.tests.utils import ensure_no_addon_upgrades


class TestFullUpgrade(IntranettTestCase):

    def test_list_steps(self):
        setup = getToolByName(self.portal, "portal_setup")
        upgrades = ensure_no_addon_upgrades(setup)
        for profile, steps in upgrades.items():
            self.assertEquals(len(steps), 0,
                              "Found unexpected upgrades: %s" % steps)

    def test_do_upgrades(self):
        setup = getToolByName(self.portal, "portal_setup")
        self.setRoles(['Manager'])

        setup.setLastVersionForProfile(POLICY_PROFILE, '1')
        setup.setLastVersionForProfile(THEME_PROFILE, '1')

        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) > 0)

        run_upgrade(setup, THEME_PROFILE)
        run_upgrade(setup)

        # And we have reached our current profile version
        self.assertTrue(compare_profile_versions(setup, THEME_PROFILE))
        self.assertTrue(compare_profile_versions(setup, POLICY_PROFILE))

        # There are no more upgrade steps available
        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) == 0)

        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.failUnless(len(upgrades) == 0)
