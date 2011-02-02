from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestUpgradeSteps(IntranettTestCase):

    def test_activate_clamav(self):
        from intranett.policy.upgrades.steps import activate_clamav
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        clamav = ptool.clamav_properties
        clamav._updateProperty('clamav_connection', 'net')
        activate_clamav(portal)
        self.assertEqual(clamav.getProperty('clamav_connection'), 'socket')
        self.assertEqual(
            clamav.getProperty('clamav_socket'), '/var/run/clamav/clamd.sock')

    def test_disable_folderish_sections(self):
        from ..steps import disable_nonfolderish_sections
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        site_properties = ptool.site_properties
        site_properties.disable_nonfolderish_sections = False
        disable_nonfolderish_sections(portal)
        self.assertTrue(
            site_properties.getProperty('disable_nonfolderish_sections'))

    def test_activate_collective_flag(self):
        from ..steps import activate_collective_flag
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        catalog.delIndex('flaggedobject')
        activate_collective_flag(portal)
        self.assertTrue('flaggedobject' in catalog.indexes())

