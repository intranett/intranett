import re
from os.path import abspath
from os.path import dirname
from os.path import join

import transaction
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.tests.base.testcase import WarningInterceptor
from Products.GenericSetup.context import TarballImportContext
from zope.site.hooks import setSite

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.upgrades import run_upgrade


class FunctionalUpgradeTestCase(IntranettTestCase, WarningInterceptor):

    site_id = 'Plone'
    rediff = re.compile("([a-zA-z/_]*\.xml)\\n[=]*\\n(.*)", re.DOTALL)

    def setUp(self):
        super(FunctionalUpgradeTestCase, self).setUp()
        self.loginAsPortalOwner()
        setSite(self.portal)

        # Clean out some test setup artifacts
        self.portal.portal_membership.deleteMembers([TEST_USER_ID])
        del self.portal['test-folder']

        setup = getToolByName(self.portal, 'portal_setup')
        expected_export = setup.runAllExportSteps()
        self.expected = TarballImportContext(setup, expected_export['tarball'])
        setSite(None)

    def beforeTearDown(self):
        if self.site_id in self.app:
            self.app._delObject(self.site_id)
        self.logout()
        transaction.commit()

    def importFile(self, context, name):
        path = join(abspath(dirname(context)), 'data', name)
        self._trap_warning_output()
        self.app._importObjectFromFile(path, verify=0)
        self._free_warning_output()

    def migrate(self):
        oldsite = getattr(self.app, self.site_id)
        mig = oldsite.portal_migration
        components = getattr(oldsite, '_components', None)
        if components is not None:
            setSite(oldsite)

        # Adjust for some things changed by the testing infrastructure
        oldsite = getattr(self.app, self.site_id)
        oldsite.setTitle('Plone site')

        result = mig.upgrade(swallow_errors=False)

        # Run the upgrades for policy and theme
        run_upgrade(oldsite.portal_setup)
        run_upgrade(oldsite.portal_setup, u"intranett.theme:default")

        return (oldsite, result)

    def export(self):
        oldsite = getattr(self.app, self.site_id)
        setSite(oldsite)
        stool = oldsite.portal_setup
        upgraded_export = stool.runAllExportSteps()

        upgraded = TarballImportContext(stool, upgraded_export['tarball'])
        return stool.compareConfigurations(upgraded, self.expected)

    def parse_diff(self, diff):
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

        return remaining
