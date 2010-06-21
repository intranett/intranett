# Test if site creation works as expected

from unittest import TestSuite
from unittest import makeSuite
from intranett.policy.tests.base import IntranettTestCase


class TestSiteSetup(IntranettTestCase):

    def testInlineEditingDisabled(self):
        sp = self.portal.portal_properties.site_properties
        self.assertEqual(getattr(sp, "enable_inline_editing", True), False)


def test_suite():
    return TestSuite([
        makeSuite(TestSiteSetup),
    ])
