import os

from OFS.Image import Image
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.test_userdata import TEST_IMAGES
from intranett.policy.tests.utils import make_file_upload


class TestUpgradeSteps(IntranettTestCase):

    def test_activate_clamav(self):
        from ..steps import activate_clamav
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

    def test_activate_iw_rejectanonymous(self):
        from intranett.policy.setuphandlers import setup_reject_anonymous
        from iw.rejectanonymous import IPrivateSite
        from zope.interface import noLongerProvides
        portal = self.layer['portal']
        setup = getToolByName(portal, 'portal_setup')
        noLongerProvides(portal, IPrivateSite)
        self.assertFalse(IPrivateSite.providedBy(portal))
        setup_reject_anonymous(setup)
        self.assertTrue(IPrivateSite.providedBy(portal))

    def test_install_MemberData_type(self):
        from ..steps import install_MemberData_type
        portal = self.layer['portal']
        types = getToolByName(portal, 'portal_types')
        del types['MemberData']
        install_MemberData_type(portal)
        self.assertTrue('MemberData' in types)

    def test_update_caching_config(self):
        from ..steps import update_caching_config
        portal = self.layer['portal']
        registry = getToolByName(portal, 'portal_registry')
        purge_key = 'plone.app.caching.interfaces.IPloneCacheSettings.' \
            'purgedContentTypes'
        etag_key = 'plone.app.caching.weakCaching.etags'
        registry.records[purge_key].value = ('Document', )
        registry.records[etag_key].value = ('userid', 'language', )
        update_caching_config(portal)
        self.assertEqual(registry.records[purge_key].value,
            ('File', 'Image', 'News Item'))
        self.assertTrue('editbar' in registry.records[etag_key].value)

    def test_migrate_portraits(self):
        from ..steps import migrate_portraits
        from intranett.policy.tools import Portrait
        portal = self.layer['portal']

        mdt = getToolByName(portal, 'portal_memberdata')
        path = os.path.join(TEST_IMAGES, 'test.jpg')
        image_jpg = make_file_upload(path, 'image/jpeg', 'myportrait.jpg')

        image = Image(id=TEST_USER_ID, file=image_jpg, title='')
        thumb = Image(id=TEST_USER_ID, file=image_jpg, title='')
        mdt._setPortrait(image, TEST_USER_ID)
        mdt._setPortrait(thumb, TEST_USER_ID, thumbnail=True)

        migrate_portraits(portal)

        self.assertTrue(TEST_USER_ID in mdt.portraits)
        self.assertTrue(TEST_USER_ID in mdt.thumbnails)
        self.assertTrue(isinstance(mdt.portraits[TEST_USER_ID], Portrait))
        self.assertTrue(isinstance(mdt.thumbnails[TEST_USER_ID], Portrait))
