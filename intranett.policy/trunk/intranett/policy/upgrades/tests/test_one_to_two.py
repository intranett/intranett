from Products.CMFCore.utils import getToolByName

from intranett.policy.upgrades.tests.base import FunctionalUpgradeTestCase
from intranett.policy.upgrades.tests.utils import ensure_no_addon_upgrades


class TestFunctionalMigrations(FunctionalUpgradeTestCase):

    def test_gs_diff(self):
        self.importFile(__file__, 'one.zexp')
        oldsite, result = self.migrate()

        diff = self.export()
        remaining = self.parse_diff(diff)

        # self.assertEquals(set(remaining.keys()), set([]),
        #                   "Unexpected diffs in:\n %s" % remaining.items())

    def test_list_steps_for_addons(self):
        self.importFile(__file__, 'one.zexp')
        oldsite, result = self.migrate()

        setup = getToolByName(oldsite, "portal_setup")
        upgrades = ensure_no_addon_upgrades(setup)
        for profile, steps in upgrades.items():
            self.assertEquals(len(steps), 0,
                              "Found unexpected upgrades: %s" % steps)
