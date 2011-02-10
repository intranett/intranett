# -*- coding:utf-8 -*-
import os
import transaction

from Acquisition import aq_get
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility

from .utils import make_file_upload
from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.base import IntranettFunctionalTestCase

TEST_IMAGES = os.path.join(os.path.dirname(__file__), 'images')


class TestMemberTools(IntranettTestCase):

    def test_membership_tool_registered(self):
        # Check we can get the tool by name
        from ..tools import MembershipTool
        portal = self.layer['portal']
        tool = getToolByName(portal, 'portal_membership')
        self.failUnless(isinstance(tool, MembershipTool))

    def test_memberdata_tool_registered(self):
        # Check we can get the tool by name
        from ..tools import MemberDataTool
        portal = self.layer['portal']
        tool = getToolByName(portal, 'portal_memberdata')
        self.failUnless(isinstance(tool, MemberDataTool))
        from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
        self.failUnless(isinstance(tool.thumbnails, BTreeFolder2))


class TestUserdataSchema(IntranettTestCase):

    def test_no_homepage(self):
        from ..userdataschema import ICustomUserDataSchema
        self.assert_('home_page' not in ICustomUserDataSchema.names())

    def test_custom_schema(self):
        from ..userdataschema import ICustomUserDataSchema
        from plone.app.users.userdataschema import IUserDataSchemaProvider
        util = queryUtility(IUserDataSchemaProvider)
        schema = util.getSchema()
        self.assertEquals(schema, ICustomUserDataSchema)

    def test_memberdatafields(self):
        from plone.app.users.userdataschema import IUserDataSchemaProvider
        util = queryUtility(IUserDataSchemaProvider)
        schema = util.getSchema()
        self.failUnless('position' in schema)
        self.failUnless('department' in schema)
        self.failUnless('phone' in schema)
        self.failUnless('mobile' in schema)

    def test_memberinfo(self):
        from DateTime import DateTime
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'phone': '12345',
                                    'mobile': '67890',
                                    'position': 'Øngønør',
                                    'department': 'it',
                                    'email': 'info@jarn.com',
                                    'birth_date': DateTime('23/11/2008'),
                                    'description': "<p>Kjære Python!</p>"})

        info = mt.getMemberInfo()
        self.assertEquals(info['phone'], '12345')
        self.assertEquals(info['mobile'], '67890')
        self.assertEquals(info['position'], 'Øngønør')
        self.assertEquals(info['department'], 'it')
        self.assertEquals(info['email'], 'info@jarn.com')
        self.assertEquals(info['birth_date'], DateTime('23/11/2008'))
        self.assertEquals(info['description'], "<p>Kjære Python!</p>")
        info = mt.getMemberInfo(memberId='foo')
        self.failUnless(info is None)

    def test_safe_transform_description(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'description': """
            <script> document.load(something) </script>
            <object> some object </object>
            <span>This is ok</span>
        """})
        info = mt.getMemberInfo()
        self.assertEquals(info['description'].strip(), "<span>This is ok</span>")

    def test_personal_information_widget(self):
        from zope.component import getMultiAdapter
        from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
        portal = self.layer['portal']
        request = self.layer['request']
        view = getMultiAdapter((portal, request), name='personal-information')
        self.assertEquals(view.form_fields['description'].custom_widget,
                          WYSIWYGWidget)

    def test_user_information_widget(self):
        from zope.component import getMultiAdapter
        from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
        portal = self.layer['portal']
        request = self.layer['request']
        view = getMultiAdapter((portal, request), name='user-information')
        self.assertEquals(view.form_fields['description'].custom_widget,
                        WYSIWYGWidget)

    def test_userpanel(self):
        from ..userdataschema import ICustomUserDataSchema
        portal = self.layer['portal']
        panel = ICustomUserDataSchema(portal)

        self.assertEquals(panel.fullname, u'')
        panel.fullname = u'Geir Bœkholly'
        self.assertEquals(panel.fullname, u'Geir Bœkholly')

        self.assertEquals(panel.position, u'')
        panel.position = u'Øngønør'
        self.assertEquals(panel.position, u'Øngønør')

        self.assertEquals(panel.department, u'')
        panel.department = u'IT Tønsberg'
        self.assertEquals(panel.department, u'IT Tønsberg')

        self.assertEquals(panel.location, u'')
        panel.location = u'Tønsberg'
        self.assertEquals(panel.location, u'Tønsberg')

        self.assertEquals(panel.phone, '')
        panel.phone = '+47 55533'
        self.assertEquals(panel.phone, '+47 55533')

        self.assertEquals(panel.mobile, '')
        panel.mobile = '+47 55533'
        self.assertEquals(panel.mobile, '+47 55533')


class TestUserPortraits(IntranettTestCase):

    def test_set_portraits(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        mdt = getToolByName(portal, 'portal_memberdata')
        path = os.path.join(TEST_IMAGES, 'test.jpg')
        image_jpg = make_file_upload(path, 'image/jpeg', 'myportrait.jpg')
        mt.changeMemberPortrait(image_jpg)
        self.failUnless(TEST_USER_ID in mdt.portraits)
        self.failUnless(TEST_USER_ID in mdt.thumbnails)

        portrait_thumb = mt.getPersonalPortrait()
        from ..tools import PORTRAIT_SIZE, PORTRAIT_THUMBNAIL_SIZE
        self.assertEquals(portrait_thumb.width, PORTRAIT_THUMBNAIL_SIZE[0])
        self.assertEquals(portrait_thumb.height, PORTRAIT_THUMBNAIL_SIZE[1])
        portrait = mt.getPersonalPortrait(thumbnail=False)
        self.assertEquals(portrait.width, PORTRAIT_SIZE[0])
        self.assertEquals(portrait.height, PORTRAIT_SIZE[1])

    def test_change_portraits(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        path = os.path.join(TEST_IMAGES, 'test.jpg')
        image_jpg = make_file_upload(path, 'image/jpeg', 'myportrait.jpg')
        mt.changeMemberPortrait(image_jpg)
        portrait = mt.getPersonalPortrait(thumbnail=False)
        old_portrait_size = portrait.get_size()
        portrait = mt.getPersonalPortrait(thumbnail=True)
        old_thumbnail_size = portrait.get_size()

        # Now change the portraits
        path = os.path.join(TEST_IMAGES, 'test.gif')
        image_gif = make_file_upload(path, 'image/gif', 'myportrait.gif')
        mt.changeMemberPortrait(image_gif)
        portrait = mt.getPersonalPortrait(thumbnail=False)
        self.failIfEqual(old_portrait_size, portrait.get_size())
        portrait = mt.getPersonalPortrait(thumbnail=True)
        self.failIfEqual(old_thumbnail_size, portrait.get_size())

    def test_delete_portraits(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        mdt = getToolByName(portal, 'portal_memberdata')
        path = os.path.join(TEST_IMAGES, 'test.jpg')
        image_jpg = make_file_upload(path, 'image/jpeg', 'myportrait.jpg')
        mt.changeMemberPortrait(image_jpg)
        # Now delete the portraits
        mt.deletePersonalPortrait()
        self.failIf(TEST_USER_ID in mdt.portraits)
        self.failIf(TEST_USER_ID in mdt.thumbnails)

    def test_funky_ids(self):
        # Well, let's admit we really do this for the coverage.
        # There is this retarded check in changeMemberPortrait
        # that we copied and have to cover.
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        mt.getPersonalPortrait(id='')
        path = os.path.join(TEST_IMAGES, 'test.gif')
        image_gif = make_file_upload(path, 'image/gif', 'myportrait.gif')
        mt.changeMemberPortrait(image_gif, id='')


class TestImageCropping(IntranettTestCase):

    def test_image_crop(self):
        from intranett.policy.tools import crop_and_scale_image
        from PIL import Image as PILImage
        path = os.path.join(TEST_IMAGES, 'idiot.jpg')
        old_image = open(path)
        new_image_data, mimetype = crop_and_scale_image(old_image)
        new_image = PILImage.open(new_image_data)
        self.assertEqual(new_image.size, (100, 100))


class TestUserSearch(IntranettTestCase):

    def test_type(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        self.assertEqual(member.meta_type, 'MemberData')
        self.assertEqual(member.portal_type, 'MemberData')
        self.assertEqual(member.Type(), 'MemberData')

    def test_title(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'John Døe'})
        self.assertEqual(member.Title(), 'John Døe')

    def test_description(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'position': '', 'department': ''})
        self.assertEqual(member.Description(), '')
        member.setMemberProperties({'position': '', 'department': 'Øl'})
        self.assertEqual(member.Description(), 'Øl')
        member.setMemberProperties({'position': 'Tørst', 'department': ''})
        self.assertEqual(member.Description(), 'Tørst')
        member.setMemberProperties({'position': 'Tørst', 'department': 'Øl'})
        self.assertEqual(member.Description(), 'Tørst, Øl')

    def test_update_member_and_search(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'John Døe',
                                    'phone': '12345',
                                    'mobile': '67890',
                                    'position': 'Øngønør',
                                    'department': 'Tøst',
                                    'location': 'Tønsberg',
                                    'email': 'info@jarn.com',
                                    'description': '<p>Kjære Python!</p>'})
        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog.searchResults(Title='Døe')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')
        self.assertEquals(john_brain.Title, 'John Døe')
        self.assertEquals(john_brain.Description, 'Øngønør, Tøst')
        results = catalog.searchResults(SearchableText='12345')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')
        results = catalog.searchResults(SearchableText='67890')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')
        results = catalog.searchResults(SearchableText='Øngønør')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')
        results = catalog.searchResults(SearchableText='Tøst')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')
        results = catalog.searchResults(SearchableText='Tønsberg')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')
        results = catalog.searchResults(SearchableText='info@jarn.com')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')
        results = catalog.searchResults(SearchableText='Kjære')
        self.assertEquals(len(results), 1)
        john_brain = results[0]
        self.assertEquals(john_brain.getPath(), '/plone/author/test_user_1_')

    def test_safe_transform_searchable_text(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'description': '<p>Kjære Python!</p>'})
        self.assertEquals(member.SearchableText().strip(), 'Kjære Python!')

    def test_getObject(self):
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'John Døe'})
        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog.searchResults(Title='Døe')
        self.assertEquals(len(results), 1)
        brain = results[0]
        obj = brain.getObject()
        self.assertEqual(obj.Title(), 'John Døe')
        self.assertEqual(obj.getPhysicalPath(), ('', 'plone', 'user', 'test_user_1_'))


class TestFunctionalUserSearch(IntranettFunctionalTestCase):

    def test_ttw_editing(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = False
        portal = self.layer['portal']
        browser.open(portal.absolute_url() + '/@@personal-information')
        browser.getControl(name='form.fullname').value = 'John Døe'
        browser.getControl(name='form.email').value = 'test@example.com'
        browser.getControl(name='form.description').value = '<p>Kjære Python!</p>'
        browser.getControl(name='form.location').value = 'Tønsberg'
        browser.getControl(name='form.position').value = 'Øngønør'
        browser.getControl(name='form.department').value = 'Tåst'
        browser.getControl(name='form.actions.save').click()
        self.assert_(browser.url.endswith('@@personal-information'))

    def test_ttw_search(self):
        browser = get_browser(self.layer['app'])
        browser.handleErrors = False
        portal = self.layer['portal']
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'Bob Døe',
                                    'phone': '12345',
                                    'mobile': '67890',
                                    'position': 'Øngønør',
                                    'department': 'Tøst',
                                    'location': 'Tønsberg',
                                    'email': 'info@jarn.com'})
        transaction.commit()
        browser.open(portal.absolute_url())
        browser.getControl(name='SearchableText').value = 'Døe'
        browser.getForm(name='searchform').submit()
        self.failUnless('Bob Døe' in browser.contents)
        self.failUnless('Øngønør' in browser.contents)
        self.failUnless('Tøst' in browser.contents)
        self.failUnless('Øngønør, Tøst' in browser.contents)


class TestDashboard(IntranettTestCase):

    def test_default_dashboard(self):
        from plone.portlets.constants import USER_CATEGORY
        from plone.portlets.interfaces import IPortletManager

        portal = self.layer['portal']
        addUser = aq_get(portal, 'acl_users').userFolderAddUser
        addUser('member', 'secret', ['Member'], [])

        prefix = 'plone.dashboard'
        for i in range(1, 5):
            name = prefix + str(i)
            column = queryUtility(IPortletManager, name=name)
            category = column.get(USER_CATEGORY, None)
            manager = category.get('member', {})
            self.assert_(manager == {}, 'Found unexpected portlets in '
                         'dashboard column %s: %s' % (i, manager.keys()))
