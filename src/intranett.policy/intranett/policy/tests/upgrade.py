import re
from os.path import abspath
from os.path import dirname
from os.path import join
from pprint import pprint

from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.context import TarballImportContext
from zope.site.hooks import setSite

from intranett.policy.config import config
from intranett.policy.tests.utils import ensure_no_upgrades
from intranett.policy.tests.utils import suppress_warnings


class UpgradeTests(object):

    level = 2
    site_id = 'Plone'
    rediff = re.compile("([a-zA-z/_]*\.xml)\\n[=]*\\n(.*)", re.DOTALL)

    def setUp(self):
        app = self.layer['app']
        login(app, SITE_OWNER_NAME)
        portal = self.layer['portal']
        setSite(portal)

        # Clean out some test setup artifacts
        portal.portal_membership.deleteMembers([TEST_USER_ID])
        del portal['test-folder']

        setup = getToolByName(portal, 'portal_setup')
        expected_export = setup.runAllExportSteps()
        self.expected = TarballImportContext(setup, expected_export['tarball'])
        setSite(None)

    def tearDown(self):
        app = self.layer['app']
        if self.site_id in app:
            del app[self.site_id]
        logout()

    @suppress_warnings
    def importFile(self, context, name):
        path = join(abspath(dirname(context)), 'data', name)
        self.layer['app']._importObjectFromFile(path, verify=0)

    def export(self):
        portal = self.layer['portal']
        setup = portal.portal_setup
        upgraded_export = setup.runAllExportSteps()

        upgraded = TarballImportContext(setup, upgraded_export['tarball'])
        return setup.compareConfigurations(upgraded, self.expected)

    def parse_diff(self, diff):
        strings = [f for f in diff.split('Index: ') if f]
        files = {}
        for s in strings:
            if s.startswith('structure'):
                continue
            name, content = self.rediff.match(s).groups()
            files[name] = content

        # There's a couple files where we get diffs for ordering changes,
        # but the order is not important
        expected_diff = set([
            'browserlayer.xml', # fails randomly on ordering
            'portlets.xml',
            'registry.xml',
            'types/FieldsetFolder.xml',
            'types/FormFolder.xml',
            'viewlets.xml',
        ])

        remaining = {}
        for n, v in files.items():
            if n not in expected_diff:
                remaining[n] = v # pragma: no cover

        return remaining

    def test_upgrades(self):
        self.importFile(__file__, 'six.zexp')
        portal = getattr(self.layer['app'], self.site_id)

        # TODO - we should do this in a layer
        self.layer['portal'] = portal
        setSite(portal)
        self.portal = portal

        # Adjust for some things changed by the testing infrastructure
        portal.setTitle('Plone site')

        portal.portal_migration.upgrade(swallow_errors=False)
        setup = getToolByName(portal, "portal_setup")
        config.run_all_upgrades(setup, skip_policy=True)

        # run the upgrade steps for the policy
        request = self.layer['request']
        request['profile_id'] = config.policy_profile
        upgrades = setup.listUpgrades(config.policy_profile)
        for u in upgrades:
            dest = u['sdest']
            before_name = "before_%s" % dest
            before = getattr(self, before_name, None)
            if before is not None:
                before()
            request.form['upgrades'] = [u['id']]
            setup.manage_doUpgrades(request=request)
            after_name = "after_%s" % dest
            after = getattr(self, after_name, None)
            self.assertFalse(after is None,
                "The %s class is missing the %s function to check the upgrade "
                "to version %s" % (self.__class__.__name__,
                    after_name, dest))
            after()

        # test the end result
        upgrades = ensure_no_upgrades(setup)
        for profile, steps in upgrades.items():
            self.assertEquals(len(steps), 0,
                              "Found unexpected upgrades: %s" % steps)

        login(self.layer['app'], SITE_OWNER_NAME)
        diff = self.export()
        remaining = self.parse_diff(diff)

        def _print(values): # pragma: no cover
            for v in values:
                pprint(v.split('\n'))
        self.assertEqual(set(remaining.keys()), set([]),
            _print(remaining.values()))
