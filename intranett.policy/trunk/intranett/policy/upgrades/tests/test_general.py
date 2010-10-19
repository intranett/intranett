from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.upgrades import run_upgrade
from intranett.policy.upgrades.tests.base import FunctionalUpgradeTestCase

POLICY_PROFILE = u"intranett.policy:default"
CMF_PROFILE = u"Products.CMFDefault:default"
PAI_PROFILE = u"plone.app.iterate:plone.app.iterate"


def ensure_no_addon_upgrades(setup):
    profiles = set(setup.listProfilesWithUpgrades())
    # Don't test our own profile twice
    profiles.remove(POLICY_PROFILE)
    # We don't care about the CMFDefault profile in Plone
    profiles.remove(CMF_PROFILE)
    # The iterate profile has a general reinstall profile in it, we ignore
    # it since we don't use iterate
    profiles.remove(PAI_PROFILE)
    upgrades = {}
    for profile in profiles:
        upgrades[profile] = setup.listUpgrades(profile)
    return upgrades


class TestFullUpgrade(IntranettTestCase):

    def test_list_steps(self):
        # There should be no upgrade steps from the current version
        setup = getToolByName(self.portal, "portal_setup")
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.assertEquals(len(upgrades), 0,
                          "Found unexpected upgrades: %s" % upgrades)

    def test_list_steps_for_addons(self):
        setup = getToolByName(self.portal, "portal_setup")
        upgrades = ensure_no_addon_upgrades(setup)
        for profile, steps in upgrades.items():
            self.assertEquals(len(steps), 0,
                              "Found unexpected upgrades: %s" % steps)

    def test_do_upgrades(self):
        setup = getToolByName(self.portal, "portal_setup")
        self.setRoles(['Manager'])

        setup.setLastVersionForProfile(POLICY_PROFILE, '1')
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.failUnless(len(upgrades) > 0)

        run_upgrade(setup)

        # And we have reached our current profile version
        current = setup.getVersionForProfile(POLICY_PROFILE)
        current = tuple(current.split('.'))
        last = setup.getLastVersionForProfile(POLICY_PROFILE)
        self.assertEquals(last, current)

        # There are no more upgrade steps available
        upgrades = setup.listUpgrades(POLICY_PROFILE)
        self.failUnless(len(upgrades) == 0)


class TestFunctionalMigrationsFromVersion2(FunctionalUpgradeTestCase):

    def test_gs_diff(self):
        self.importFile(__file__, 'two.zexp')
        oldsite, result = self.migrate()

        diff = self.export()
        strings = [f for f in diff.split('Index: ') if f]
        files = {}
        for s in strings:
            name, content = self.rediff.match(s).groups()
            files[name] = content

        # There's a couple files where we get diffs for ordering changes,
        # but the order is not important
        expected_diff = set([
            'portlets.xml',
            'registry.xml',
            'structure/acl_users/portal_role_manager.xml',
            'types/FieldsetFolder.xml',
            'types/FormFolder.xml',
            'viewlets.xml',
        ])

        # XXX These actually do show us real problems
        expected_diff.add('properties.xml')
        expected_diff.add('actions.xml')

        remaining = {}
        for n, v in files.items():
            if n not in expected_diff:
                remaining[n] = v # pragma: no cover

        self.assertEquals(set(files.keys()) - expected_diff, set([]),
                          "Unexpected diffs in:\n %s" % remaining.items())

    def test_list_steps_for_addons(self):
        self.importFile(__file__, 'two.zexp')
        oldsite, result = self.migrate()

        setup = getToolByName(oldsite, "portal_setup")
        upgrades = ensure_no_addon_upgrades(setup)
        for profile, steps in upgrades.items():
            self.assertEquals(len(steps), 0,
                              "Found unexpected upgrades: %s" % steps)
