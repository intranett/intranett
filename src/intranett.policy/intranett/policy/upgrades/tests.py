import os

from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager
from zope.component import queryUtility

from intranett.policy.upgrades import steps
from intranett.policy.tests.base import IntranettTestCase


class TestUpgradeSteps(IntranettTestCase):

    def test_activate_clamav(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        clamav = ptool.clamav_properties
        clamav._updateProperty('clamav_connection', 'net')
        steps.activate_clamav(portal)
        self.assertEqual(clamav.getProperty('clamav_connection'), 'socket')
        self.assertEqual(
            clamav.getProperty('clamav_socket'), '/var/run/clamav/clamd.sock')

    def test_disable_folderish_sections(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        site_properties = ptool.site_properties
        site_properties.disable_nonfolderish_sections = False
        steps.disable_nonfolderish_sections(portal)
        self.assertTrue(
            site_properties.getProperty('disable_nonfolderish_sections'))

    def test_activate_collective_flag(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        catalog.delIndex('flaggedobject')
        steps.activate_collective_flag(portal)
        self.assertTrue('flaggedobject' in catalog.indexes())

    def test_activate_iw_rejectanonymous(self):
        from iw.rejectanonymous import IPrivateSite
        from zope.interface import noLongerProvides
        portal = self.layer['portal']
        setup = getToolByName(portal, 'portal_setup')
        noLongerProvides(portal, IPrivateSite)
        self.assertFalse(IPrivateSite.providedBy(portal))
        steps.setup_reject_anonymous(setup)
        self.assertTrue(IPrivateSite.providedBy(portal))

    def test_install_memberdata_type(self):
        portal = self.layer['portal']
        types = getToolByName(portal, 'portal_types')
        del types['MemberData']
        steps.install_memberdata_type(portal)
        self.assertTrue('MemberData' in types)

    def test_update_caching_config(self):
        portal = self.layer['portal']
        registry = getToolByName(portal, 'portal_registry')
        purge_key = 'plone.app.caching.interfaces.IPloneCacheSettings.' \
            'purgedContentTypes'
        etag_key = 'plone.app.caching.weakCaching.etags'
        registry.records[purge_key].value = ('Document', )
        registry.records[etag_key].value = ('userid', 'language', )
        steps.update_caching_config(portal)
        self.assertEqual(registry.records[purge_key].value,
            ('File', 'Image', 'News Item'))
        self.assertTrue('editbar' in registry.records[etag_key].value)

    def test_migrate_portraits(self):
        from OFS.Image import Image
        from intranett.policy.tests.test_userdata import TEST_IMAGES
        from intranett.policy.tests.utils import make_file_upload
        from intranett.policy.tools import Portrait

        portal = self.layer['portal']

        mdt = getToolByName(portal, 'portal_memberdata')
        path = os.path.join(TEST_IMAGES, 'test.jpg')
        image_jpg = make_file_upload(path, 'image/jpeg', 'myportrait.jpg')

        image = Image(id=TEST_USER_ID, file=image_jpg, title='')
        thumb = Image(id=TEST_USER_ID, file=image_jpg, title='')
        mdt._setPortrait(image, TEST_USER_ID)
        mdt._setPortrait(thumb, TEST_USER_ID, thumbnail=True)

        steps.migrate_portraits(portal)

        self.assertTrue(TEST_USER_ID in mdt.portraits)
        self.assertTrue(TEST_USER_ID in mdt.thumbnails)
        self.assertTrue(isinstance(mdt.portraits[TEST_USER_ID], Portrait))
        self.assertTrue(isinstance(mdt.thumbnails[TEST_USER_ID], Portrait))

    def test_disable_webstats_js(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        sprops = ptool.site_properties
        sprops.webstats_js = '<script type="text/javascript" />'
        steps.disable_webstats_js(portal)
        self.assertEqual(sprops.webstats_js, '')

    def test_remove_unused_frontpage_portlets(self):
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.manager import PortletManager
        portal = self.layer['portal']
        sm = getSiteManager()
        names = ('frontpage.portlets.left', 'frontpage.portlets.central',
            'frontpage.bottom')
        def create_pm(name):
            sm.registerUtility(component=PortletManager(),
                provided=IPortletManager, name=name)
        for name in names:
            create_pm(name)
        steps.remove_unused_frontpage_portlets(portal)
        registrations = [r.name for r in sm.registeredUtilities()
                         if IPortletManager == r.provided]
        self.assertFalse('frontpage.portlets.left' in registrations)
        self.assertFalse('frontpage.portlets.central' in registrations)
        self.assertFalse('frontpage.bottom' in registrations)

    def test_add_site_administrator(self):
        portal = self.layer['portal']
        existing_roles = set(getattr(portal, '__ac_roles__', []))
        existing_roles.remove('Site Administrator')
        portal.__ac_roles__ = tuple(existing_roles)
        steps.add_site_administrator(portal)
        existing_roles = set(getattr(portal, '__ac_roles__', []))
        self.assertIn('Site Administrator', existing_roles)

    def test_allow_site_admin_to_edit_frontpage(self):
        from plone.portlets.interfaces import IPortletType
        from plone.app.portlets.interfaces import IColumn
        portal = self.layer['portal']
        setattr(portal, '_Portlets__Manage_portlets_Permission', ['Manager'])
        fti = getToolByName(portal, 'portal_types')['Plone Site']
        edit_action = [a for a in fti.listActions() if a.id == 'edit-frontpage']
        edit_action[0].permissions = ('Manage portal', )
        coll_id = u'plone.portlet.collection.Collection'
        coll = queryUtility(IPortletType, name=coll_id)
        coll.for_ = [IColumn]
        steps.allow_site_admin_to_edit_frontpage(portal)
        perms = set(getattr(portal, '_Portlets__Manage_portlets_Permission'))
        self.assertEqual(perms, set(['Manager', 'Site Administrator']))
        self.assertEqual(edit_action[0].permissions,
            (u'Portlets: Manage portlets', ))
        self.assertEqual(coll.for_, [])

    def test_allow_member_to_edit_personal_portlets(self):
        portal = self.layer['portal']
        perm_id = '_plone_portlet_static__Add_static_portlet_Permission'
        setattr(portal, perm_id, ['Manager'])
        steps.allow_member_to_edit_personal_portlets(portal)
        self.assertEqual(set(getattr(portal, perm_id)),
            set(['Manager', 'Member', 'Site Administrator']))
