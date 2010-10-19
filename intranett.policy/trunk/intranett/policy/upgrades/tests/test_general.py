from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase

POLICY_PROFILE = "intranett.policy:default"


class TestFullUpgrade(IntranettTestCase):

    def test_list_steps(self):
        # There should be no upgrade steps from the current version
        setup = getToolByName(self.portal, "portal_setup")
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.failUnless(len(upgrades) == 0)

    def test_do_upgrades(self):
        setup = getToolByName(self.portal, "portal_setup")
        self.setRoles(['Manager'])

        setup.setLastVersionForProfile(POLICY_PROFILE, '1')
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.failUnless(len(upgrades) > 0)

        request = self.portal.REQUEST
        request.form['profile_id'] = POLICY_PROFILE

        steps = []
        for u in upgrades:
            if isinstance(u, list): # pragma: no cover
                steps.extend([s['id'] for s in u])
            else:
                steps.append(u['id'])

        request.form['upgrades'] = steps
        setup.manage_doUpgrades(request=request)

        # And we have reached our current profile version
        current = setup.getVersionForProfile(POLICY_PROFILE)
        current = tuple(current.split('.'))
        last = setup.getLastVersionForProfile(POLICY_PROFILE)
        self.assertEquals(last, current)

        # There are no more upgrade steps available
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.failUnless(len(upgrades) == 0)
