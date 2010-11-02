from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy.config import POLICY_PROFILE
from intranett.policy.tests.base import IntranettTestCase
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
        portal = self.layer['portal']
        setup = getToolByName(portal, "portal_setup")
        setRoles(portal, TEST_USER_ID, ['Manager'])

        setup.setLastVersionForProfile(POLICY_PROFILE, '1')
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        # TODO: Enable again once we have upgrade steps
        # self.failUnless(len(upgrades) > 0)

        run_upgrade(setup)

        # And we have reached our current profile version
        current = setup.getVersionForProfile(POLICY_PROFILE)
        current = tuple(current.split('.'))
        last = setup.getLastVersionForProfile(POLICY_PROFILE)
        self.assertEquals(last, current)

        # There are no more upgrade steps available
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.failUnless(len(upgrades) == 0)
