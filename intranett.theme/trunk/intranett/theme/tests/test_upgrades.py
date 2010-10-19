from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase

THEME_PROFILE = "intranett.theme:default"


class TestFullUpgrade(IntranettTestCase):

    def testListUpgradeSteps(self):
        # There should be no upgrade steps from the current version
        setup = getToolByName(self.portal, "portal_setup")
        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) == 0)

    def testDoUpgrades(self):
        setup = getToolByName(self.portal, "portal_setup")
        self.setRoles(['Manager'])

        setup.setLastVersionForProfile(THEME_PROFILE, '1')
        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) > 0)

        request = self.portal.REQUEST
        request.form['profile_id'] = THEME_PROFILE

        steps = []
        for u in upgrades:
            if isinstance(u, list): # pragma: no cover
                steps.extend([s['id'] for s in u])
            else:
                steps.append(u['id'])

        request.form['upgrades'] = steps
        setup.manage_doUpgrades(request=request)

        # And we have reached our current profile version
        current = setup.getVersionForProfile(THEME_PROFILE)
        current = tuple(current.split('.'))
        last = setup.getLastVersionForProfile(THEME_PROFILE)
        self.assertEquals(last, current)

        # There are no more upgrade steps available
        upgrades = setup.listUpgrades(THEME_PROFILE)
        self.failUnless(len(upgrades) == 0)
