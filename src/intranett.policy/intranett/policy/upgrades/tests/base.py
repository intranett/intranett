import re
from os.path import abspath
from os.path import dirname
from os.path import join

from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.context import TarballImportContext
from zope.site.hooks import setSite

from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.utils import suppress_warnings
from intranett.policy.upgrades import run_upgrade


class FunctionalUpgradeTestCase(IntranettFunctionalTestCase):

    site_id = 'Plone'
    rediff = re.compile("([a-zA-z/_]*\.xml)\\n[=]*\\n(.*)", re.DOTALL)

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
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

    def migrate(self):
        oldsite = getattr(self.layer['app'], self.site_id)
        mig = oldsite.portal_migration
        components = getattr(oldsite, '_components', None)
        if components is not None:
            setSite(oldsite)

        # Adjust for some things changed by the testing infrastructure
        oldsite = getattr(self.layer['app'], self.site_id)
        oldsite.setTitle('Plone site')

        result = mig.upgrade(swallow_errors=False)

        # Run the upgrades for theme and policy
        run_upgrade(oldsite.portal_setup, u"intranett.theme:default")
        run_upgrade(oldsite.portal_setup)

        return (oldsite, result)

    def export(self):
        oldsite = getattr(self.layer['app'], self.site_id)
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
            'browserlayer.xml',
            'controlpanel.xml',
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
