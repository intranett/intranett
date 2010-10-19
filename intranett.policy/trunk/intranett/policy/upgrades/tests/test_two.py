from Products.CMFCore.utils import getToolByName

from intranett.policy.upgrades.tests.base import FunctionalUpgradeTestCase
from intranett.policy.upgrades.tests.utils import ensure_no_addon_upgrades


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
