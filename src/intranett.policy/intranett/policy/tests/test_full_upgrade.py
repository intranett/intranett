from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy.config import config
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.utils import ensure_no_upgrades


class TestFullUpgrade(IntranettTestCase):

    def test_all_steps_taken(self):
        numbers = sorted(config.upgrades)
        self.assertEqual(numbers, range(min(numbers), max(numbers) + 1))

    def test_list_steps(self):
        portal = self.layer['portal']
        setup = getToolByName(portal, "portal_setup")
        upgrades = ensure_no_upgrades(setup)
        for profile, steps in upgrades.items():
            self.assertEquals(len(steps), 0,
                              "Found unexpected upgrades: %s" % steps)

    def test_do_upgrades(self):
        portal = self.layer['portal']
        setup = getToolByName(portal, "portal_setup")
        setRoles(portal, TEST_USER_ID, ['Manager'])
        setup.setLastVersionForProfile(config.policy_profile, '6')
        config.run_all_upgrades(setup)
        # There are no more upgrade steps available
        upgrades = setup.listUpgrades(config.policy_profile)
        self.assertEqual(upgrades, [])
