from os.path import abspath
from os.path import dirname
from os.path import join

import transaction
from Products.CMFCore.tests.base.testcase import WarningInterceptor
from Products.GenericSetup.context import TarballImportContext
from Testing.ZopeTestCase.sandbox import Sandboxed
from zope.site.hooks import setSite

from intranett.policy.tests.base import IntranettTestCase


class FunctionalUpgradeTestCase(Sandboxed, IntranettTestCase,
                                WarningInterceptor):

    _setup_fixture = 0
    site_id = 'Plone'

    def afterSetUp(self):
        self.loginAsPortalOwner()
        setSite(self.portal)
        stool = self.portal.portal_setup
        expected_export = stool.runAllExportSteps()
        self.expected = TarballImportContext(stool, expected_export['tarball'])
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
        result = mig.upgrade(swallow_errors=False)
        return (oldsite, result)

    def export(self):
        oldsite = getattr(self.app, self.site_id)
        setSite(oldsite)
        stool = oldsite.portal_setup
        upgraded_export = stool.runAllExportSteps()

        upgraded = TarballImportContext(stool, upgraded_export['tarball'])
        return stool.compareConfigurations(upgraded, self.expected)
