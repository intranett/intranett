from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestFullUpgrade(IntranettTestCase):

    def testListUpgradeSteps(self):
        # There should be no upgrade steps from the current version
        setup = getToolByName(self.portal, "portal_setup")
        upgrades = setup.listUpgrades("intranett.theme:default")
        self.failUnless(len(upgrades) == 0)

    def testDoUpgrades(self):
        setup = getToolByName(self.portal, "portal_setup")
        self.setRoles(['Manager'])

        setup.setLastVersionForProfile("intranett.theme:default", '1')
        upgrades = setup.listUpgrades("intranett.theme:default")
        self.failUnless(len(upgrades) > 0)

        request = self.portal.REQUEST
        request.form['profile_id'] = "intranett.theme:default"

        steps = []
        for u in upgrades:
            if isinstance(u, list): # pragma: no cover
                steps.extend([s['id'] for s in u])
            else:
                steps.append(u['id'])

        request.form['upgrades'] = steps
        setup.manage_doUpgrades(request=request)

        # And we have reached our current profile version
        current = setup.getVersionForProfile("intranett.theme:default")
        current = tuple(current.split('.'))
        last = setup.getLastVersionForProfile("intranett.theme:default")
        self.assertEquals(last, current)

        # There are no more upgrade steps available
        upgrades = setup.listUpgrades("intranett.theme:default")
        self.failUnless(len(upgrades) == 0)
