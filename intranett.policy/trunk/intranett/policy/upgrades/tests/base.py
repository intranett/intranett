import re
from os.path import abspath
from os.path import dirname
from os.path import join

import transaction
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.tests.base.testcase import WarningInterceptor
from Products.GenericSetup.context import TarballImportContext
from Products.PloneTestCase.ptc import default_user
from Testing.ZopeTestCase.sandbox import Sandboxed
from zope.site.hooks import setSite

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.upgrades import run_upgrade


class FunctionalUpgradeTestCase(Sandboxed, IntranettTestCase,
                                WarningInterceptor):

    _setup_fixture = 0
    site_id = 'Plone'
    rediff = re.compile("([a-zA-z/_]*\.xml)\\n[=]*\\n(.*)", re.DOTALL)

    def afterSetUp(self):
        self.loginAsPortalOwner()
        setSite(self.portal)

        # Clean out some test setup artifacts
        self.portal.portal_membership.deleteMembers([default_user])
        del self.portal['Members']
        skins = self.portal.portal_skins
        for s in list(skins.keys()):
            if s.startswith('sunburst'):
                del skins[s]
        del skins.selections['Sunburst Theme']

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
