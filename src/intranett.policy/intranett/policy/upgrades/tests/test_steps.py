from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestUpgradeSteps(IntranettTestCase):

    def test_disable_folderish_sections(self):
        from ..steps import disable_nonfolderish_sections
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        site_properties = ptool.site_properties
        site_properties.disable_nonfolderish_sections = False
        disable_nonfolderish_sections(portal)
        self.assertTrue(
            site_properties.getProperty('disable_nonfolderish_sections'))
