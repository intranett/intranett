# -*- coding:utf-8 -*-
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
        pass

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
        from plone.registry.interfaces import IRegistry
        registry = queryUtility(IRegistry)
        key = 'plone.app.caching.strongCaching.maxage'
        self.assertTrue(registry.get(key) >= 604800)

    def after_24(self):
        from plone.registry.interfaces import IRegistry
        registry = queryUtility(IRegistry)
        key = 'plone.app.caching.strongCaching.plone.resource.maxage'
        self.assertTrue(registry.get(key) >= 604800)

    def after_25(self):
        portal = self.layer['portal']
        users = portal.users
        self.assertNotEqual(users.Title(), portal.Title())

    def after_26(self):
        portal = self.layer['portal']
        error_log = aq_get(portal, 'error_log')
        exceptions = error_log.getProperties()['ignored_exceptions']
        self.assertTrue('LinkIntegrityNotificationException' in exceptions)

    def after_27(self):
        portal = self.layer['portal']
        atool = getToolByName(portal, 'portal_actions')
        self.assertTrue('support' in atool.site_actions)
        ids = atool.site_actions.keys()
        self.assertLessEqual(ids.index('accessibility'), ids.index('support'))

    def after_28(self):
        portal = self.layer['portal']
        tiny = getToolByName(portal, 'portal_tinymce')
        self.assertTrue(tiny.link_using_uids, True)

    def after_29(self):
        # tested by GS export diff
        pass

    def after_30(self):
        portal = self.layer['portal']
        wtool = getToolByName(portal, 'portal_workflow')
        self.assertTrue('two_state_intranett_workflow' in wtool)
        self.assertEqual(wtool.getChainFor('File'),
            ('one_state_intranett_workflow', ))
        self.assertEqual(wtool.getChainFor('Image'),
            ('one_state_intranett_workflow', ))
        self.assertEqual(wtool.getChainFor('Discussion Item'),
            ('one_state_intranett_workflow', ))

    def after_31(self):
        perm_id = '_Review_comments_Permission'
        self.assertEqual(set(getattr(self.portal, perm_id)),
            set(['Manager', 'Site Administrator', 'Reviewer']))

    def after_32(self):
        portal = self.layer['portal']
        js = getToolByName(portal, 'portal_javascripts')
        resources = [r[1] for r in js.getResourcesDict().items() if
            r[0] == 'mark_special_links.js']
        self.assertEqual(len(resources), 1)
        self.assertTrue(resources[0].getEnabled())

    def before_33(self):
        from intranett.policy.config import PERSONAL_FOLDER_ID
        portal = self.layer['portal']
        mtool = getToolByName(portal, 'portal_membership')
        mtool.addMember(u'fred', 'secret', ['Member'], [])
        self.assertFalse(PERSONAL_FOLDER_ID in portal)

    def after_33(self):
        from intranett.policy.config import PERSONAL_FOLDER_ID
        from intranett.policy.utils import quote_userid
        portal = self.layer['portal']
        self.assertTrue(PERSONAL_FOLDER_ID in portal)
        folder_id = quote_userid(u'fred')
        self.assertTrue(folder_id in portal[PERSONAL_FOLDER_ID])
        personal_folder = portal[PERSONAL_FOLDER_ID][folder_id]
        self.assertEqual(personal_folder.getOwner().getId(), u'fred')
        self.assertEqual(personal_folder.Creator(), 'fred')

    def after_34(self):
        portal = self.layer['portal']
        prefix = '++resource++plone.formwidget.autocomplete/jquery.' \
            'autocomplete'
        css = getToolByName(portal, 'portal_css')
        self.assertFalse(prefix + '.css' in css.getResourcesDict().keys())
        js = getToolByName(portal, 'portal_javascripts')
        self.assertFalse(prefix + '.min.js' in js.getResourcesDict().keys())

    def after_35(self):
        portal = self.layer['portal']
        wtool = getToolByName(portal, 'portal_workflow')
        self.assertTrue('projectroom_workflow' in wtool)
        self.assertIn('ProjectRoom', portal.portal_types)
        self.assertIn('ProjectRoom', portal.portal_factory.getFactoryTypes())
        self.assertEqual(wtool.getDefaultChain(), ('intranett_workflow',))
        self.assertEqual(wtool.getChainForPortalType("Document"), ('intranett_workflow',))
        self.assertEqual(wtool.getChainForPortalType("ProjectRoom"), ('projectroom_workflow',))
        self.assertTrue('two_state_intranett_workflow' in wtool)
        self.assertEqual(wtool.getChainFor('File'),
            ('two_state_intranett_workflow', ))
        self.assertEqual(wtool.getChainFor('Image'),
            ('two_state_intranett_workflow', ))
        self.assertEqual(wtool.getChainFor('Discussion Item'),
            ('one_state_intranett_workflow', ))

        action = portal.portal_actions.object.local_roles
        self.assertEqual(action.getProperty('available_expr'),
                "python:getattr(object, 'getProjectRoom', None) is None")

    def before_36(self):
        # simulate what happened on the actual live servers
        portal = self.layer['portal']
        ftool = getToolByName(portal, 'portal_factory')
        types = set(ftool.getFactoryTypes().keys())
        types.remove('ProjectRoom')
        ftool.manage_setPortalFactoryTypes(listOfTypeIds=list(types))

    def after_36(self):
        portal = self.layer['portal']
        ftool = getToolByName(portal, 'portal_factory')
        types = set(ftool.getFactoryTypes().keys())
        self.assertTrue('ProjectRoom' in types)
        sm = getSiteManager()
        regs = [r.name for r in sm.registeredUtilities()
                if IPortletType == r.provided]
        self.assertFalse('intranett.policy.portlets.NewsHighlight' in regs)
        self.assertFalse('intranett.policy.portlets.EventHighlight' in regs)
        self.assertFalse('intranett.policy.portlets.ContentHighlight' in regs)

    def after_37(self):
        # tested by GS export diff
        pass

    def after_38(self):
        # tested by GS export diff
        pass

    def after_39(self):
        portal = self.layer['portal']
        acl = aq_get(portal, 'acl_users')
        self.assertNotEqual(acl.session.cookie_lifetime, 0)

    def after_40(self):
        # tested by GS export diff
        pass

    def after_41(self):
        from collective.quickupload.portlet import quickuploadportlet
        sm = getSiteManager()
        regs = [r.name for r in sm.registeredUtilities()
                if IPortletType == r.provided]
        self.assertTrue('collective.quickupload.QuickUploadPortlet' in regs)
        portal = self.layer['portal']
        mapping = portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        assigned = [type(p) for p in mapping.values()]
        self.assertTrue(quickuploadportlet.Assignment in assigned)

    def after_42(self):
        portal = self.layer['portal']
        at = getToolByName(portal, 'portal_amberjack')
        self.assertTrue(at.sandbox)
        personal = portal['personal']
        mapping = personal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        self.assertTrue('amberjack-choice-portlet-skinid' in mapping)

    def after_43(self):
        portal = self.layer['portal']
        js = getToolByName(portal, 'portal_javascripts')
        resources = js.getResourcesDict()
        self.assertFalse('sarissa.js' in resources)
        self.assertFalse('++resource++MochiKit.js' in resources)
        self.assertFalse('++resource++prototype.js' in resources)
        self.assertFalse('++resource++effects.js' in resources)
        self.assertFalse('++resource++cssQuery-compat.js' in resources)
        self.assertFalse('++resource++base2-dom-fp.js' in resources)
        self.assertFalse('++resource++kukit.js' in resources)
        self.assertFalse('++resource++kukit-devel.js' in resources)
