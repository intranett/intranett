from unittest import TestSuite
from unittest import makeSuite

from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestSiteSetup(IntranettTestCase):

    def testInlineEditingDisabled(self):
        sp = self.portal.portal_properties.site_properties
        self.assertEqual(getattr(sp, "enable_inline_editing", True), False)

    def testInstallableProfiles(self):
        from Products.CMFPlone.browser.admin import AddPloneSite
        add = AddPloneSite(self.portal, self.portal.REQUEST)
        profiles = add.profiles()['extensions']
        ids = [p['id'] for p in profiles]
        self.assertEquals(ids, [u'intranett.policy:default'])

    def testInstallableProducts(self):
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        installable = qi.listInstallableProducts()
        ids = [p['id'] for p in installable]
        self.assertEquals(ids, [])


def test_suite():
    return TestSuite([
        makeSuite(TestSiteSetup),
    ])
