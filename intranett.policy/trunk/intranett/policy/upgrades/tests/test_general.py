from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.upgrades.tests.base import FunctionalUpgradeTestCase

POLICY_PROFILE = u"intranett.policy:default"
CMF_PROFILE = u"Products.CMFDefault:default"
PAI_PROFILE = u"plone.app.iterate:plone.app.iterate"


class TestFullUpgrade(IntranettTestCase):

    def test_list_steps(self):
        # There should be no upgrade steps from the current version
        setup = getToolByName(self.portal, "portal_setup")
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.assertEquals(len(upgrades), 0,
                          "Found unexpected upgrades: %s" % upgrades)

    def test_list_steps_for_addons(self):
        setup = getToolByName(self.portal, "portal_setup")
        profiles = set(setup.listProfilesWithUpgrades())
        # Don't test our own profile twice
        profiles.remove(POLICY_PROFILE)
        # We don't care about the CMFDefault profile in Plone
        profiles.remove(CMF_PROFILE)
        # The iterate profile has a general reinstall profile in it, we ignore
        # it since we don't use iterate
        profiles.remove(PAI_PROFILE)
        for profile in profiles:
            upgrades = setup.listUpgrades(profile)
            self.assertEquals(len(upgrades), 0,
                              "Found unexpected upgrades: %s" % upgrades)

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


class TestFunctionalMigrations(FunctionalUpgradeTestCase):

    def test_upgrade_from_version_two(self):
        self.importFile(__file__, 'two.zexp')
        oldsite, result = self.migrate()

        mig = oldsite.portal_migration
        self.failIf(mig.needUpgrading())

        diff = self.export()
        len_diff = len(diff.split('\n'))
        # self.failUnless(len_diff <= 2500)
