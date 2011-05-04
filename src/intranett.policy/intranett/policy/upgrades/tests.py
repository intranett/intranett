import os

from Acquisition import aq_get
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletType
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager
from zope.component import queryUtility

from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.upgrade import UpgradeTests


class TestUpgradeSteps(UpgradeTests, IntranettFunctionalTestCase):

    def before_7(self):
        registry = getToolByName(self.portal, 'portal_registry')
        etag_key = 'plone.app.caching.weakCaching.etags'
        self.assertFalse('editbar' in registry.records[etag_key].value)

    def after_7(self):
        registry = getToolByName(self.portal, 'portal_registry')
        purge_key = 'plone.app.caching.interfaces.IPloneCacheSettings.' \
            'purgedContentTypes'
        etag_key = 'plone.app.caching.weakCaching.etags'
        self.assertEqual(registry.records[purge_key].value,
            ('File', 'Image', 'News Item'))
        self.assertTrue('editbar' in registry.records[etag_key].value)

    def before_8(self):
        from OFS.Image import Image
        from intranett.policy.tests.test_userdata import TEST_IMAGES
        from intranett.policy.tests.utils import make_file_upload
        mdt = getToolByName(self.portal, 'portal_memberdata')
        path = os.path.join(TEST_IMAGES, 'test.jpg')
        image_jpg = make_file_upload(path, 'image/jpeg', 'myportrait.jpg')
        image = Image(id=TEST_USER_ID, file=image_jpg, title='')
        thumb = Image(id=TEST_USER_ID, file=image_jpg, title='')
        mdt._setPortrait(image, TEST_USER_ID)
        mdt._setPortrait(thumb, TEST_USER_ID, thumbnail=True)

    def after_8(self):
        from intranett.policy.tools import Portrait
        mdt = getToolByName(self.portal, 'portal_memberdata')
        self.assertTrue(TEST_USER_ID in mdt.portraits)
        self.assertTrue(TEST_USER_ID in mdt.thumbnails)
        self.assertTrue(isinstance(mdt.portraits[TEST_USER_ID], Portrait))
        self.assertTrue(isinstance(mdt.thumbnails[TEST_USER_ID], Portrait))

    def after_9(self):
        ptool = getToolByName(self.portal, 'portal_properties')
        self.assertEqual(ptool.site_properties.webstats_js, '')

    def after_10(self):
        sm = getSiteManager()
        registrations = [r.name for r in sm.registeredUtilities()
                         if IPortletManager == r.provided]
        self.assertFalse('frontpage.portlets.left' in registrations)
        self.assertFalse('frontpage.portlets.central' in registrations)
        self.assertFalse('frontpage.bottom' in registrations)

    def after_11(self):
        existing_roles = set(getattr(self.portal, '__ac_roles__', []))
        self.assertIn('Site Administrator', existing_roles)

    def after_12(self):
        portal = self.layer['portal']
        perms = set(getattr(portal, '_Portlets__Manage_portlets_Permission'))
        self.assertEqual(perms, set(['Manager', 'Site Administrator']))
        fti = getToolByName(portal, 'portal_types')['Plone Site']
        edit_action = [a for a in fti.listActions() if a.id == 'edit-frontpage']
        self.assertEqual(edit_action[0].permissions,
            (u'Portlets: Manage portlets', ))
        coll_id = u'plone.portlet.collection.Collection'
        coll = queryUtility(IPortletType, name=coll_id)
        self.assertEqual(coll.for_, [])

    def after_13(self):
        perm_id = '_plone_portlet_static__Add_static_portlet_Permission'
        self.assertEqual(set(getattr(self.portal, perm_id)),
            set(['Manager', 'Member', 'Site Administrator']))

    def after_14(self):
        from plone.caching.interfaces import ICacheSettings
        from plone.registry.interfaces import IRegistry
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ICacheSettings)
        value = settings.operationMapping['intranett.frontpage']
        self.assertEqual(value, 'plone.app.caching.noCaching')

    def after_15(self):
        sm = getSiteManager()
        registrations = [r.name for r in sm.registeredUtilities()
                         if IPortletManager == r.provided]
        self.assertFalse('frontpage.highlight' in registrations)
        self.assertTrue('frontpage.main.top' in registrations)

    def after_16(self):
        perm_id = '_ATContentTypes__Add_Folder_Permission'
        self.assertEqual(set(getattr(self.portal, perm_id)),
            set(['Manager', 'Contributor', 'Site Administrator', 'Owner']))

    def after_17(self):
        portal = self.layer['portal']
        sm = getSiteManager()
        regs = [r.name for r in sm.registeredUtilities()
            if r.provided == IPortletType]
        self.assertTrue('intranett.policy.portlets.NewsHighlight' in regs)
        self.assertTrue('intranett.policy.portlets.EventHighlight' in regs)
        prefix = '++resource++plone.formwidget.autocomplete/jquery.' \
            'autocomplete'
        css = getToolByName(portal, 'portal_css')
        self.assertTrue(prefix + '.css' in css.getResourcesDict().keys())
        js = getToolByName(portal, 'portal_javascripts')
        self.assertTrue(prefix + '.min.js' in js.getResourcesDict().keys())

    def after_18(self):
        portal = self.layer['portal']
        atct = getToolByName(portal, 'portal_atct')
        catalog = getToolByName(portal, 'portal_catalog')
        self.assertFalse('flaggedobject' in atct.getIndexes())
        self.assertFalse('flaggedobject' in catalog.indexes())

    def after_19(self):
        from plone.app.discussion.interfaces import IDiscussionSettings
        from plone.registry.interfaces import IRegistry
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings)
        self.assertEqual(settings.user_notification_enabled, False)

    def after_20(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        clamav = ptool.clamav_properties
        self.assertEqual(clamav.getProperty('clamav_connection'), 'net')
        self.assertEqual(
            clamav.getProperty('clamav_host'), 'jarn11.gocept.net')
        self.assertEqual(
            clamav.getProperty('clamav_port'), '3310')

    def after_21(self):
        portal = self.layer['portal']
        atool = getToolByName(portal, 'portal_actions')
        self.assertFalse('employee-listing' in atool.portal_tabs)
        self.assertTrue('users' in portal)

    def after_22(self):
        portal = self.layer['portal']
        acl = aq_get(portal, 'acl_users')
        self.assertEqual(acl.session.getProperty('secure'), True)

    def after_23(self):
        portal = self.layer['portal']
        self.assertIn('TeamWorkspace', portal.portal_types)
        self.assertIn('workspace_workflow', portal.portal_workflow)
        self.assertEqual(('intranett_workflow', 'workspace_workflow'), portal.portal_workflow.getDefaultChain())
        self.assertEqual(('intranett_workflow', 'workspace_workflow'), portal.portal_workflow.getChainForPortalType("Document"))
        
