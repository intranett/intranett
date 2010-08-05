from unittest import TestSuite
from unittest import makeSuite

from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestTheme(IntranettTestCase):

    def test_theme(self):
        skins = getToolByName(self.portal, 'portal_skins')
        self.assertEquals(skins.getDefaultSkin(), 'Intranett.no base theme')


def test_suite():
    return TestSuite([
        makeSuite(TestTheme),
    ])
