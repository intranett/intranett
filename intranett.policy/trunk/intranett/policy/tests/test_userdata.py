# -*- coding:utf-8 -*-
from Acquisition import aq_get
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.base import IntranettFunctionalTestCase
from Products.PloneTestCase.ptc import default_user


class TestMemberTools(IntranettTestCase):

    def test_membership_tool_registered(self):
        # Check we can get the tool by name
        from ..tools import MembershipTool
        tool = getToolByName(self.portal, 'portal_membership')
        self.failUnless(isinstance(tool, MembershipTool))

    def test_memberdata_tool_registered(self):
        # Check we can get the tool by name
        from ..tools import MemberDataTool
        tool = getToolByName(self.portal, 'portal_memberdata')
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
        mt = getToolByName(self.portal, 'portal_membership')
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
        mt = getToolByName(self.portal, 'portal_membership')
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
        view = getMultiAdapter((self.portal, self.app.REQUEST),
                               name='personal-information')
        self.assertEquals(view.form_fields['description'].custom_widget,
                          WYSIWYGWidget)

    def test_user_information_widget(self):
        from zope.component import getMultiAdapter
        from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
        view = getMultiAdapter((self.portal, self.app.REQUEST),
                             name='user-information')
        self.assertEquals(view.form_fields['description'].custom_widget,
                        WYSIWYGWidget)

    def test_userpanel(self):
        from ..userdataschema import ICustomUserDataSchema
        panel = ICustomUserDataSchema(self.portal)

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

    def afterSetUp(self):
        import os
        from .utils import makeFileUpload
        image_file = os.path.join(os.path.dirname(__file__), 'images', 'test.jpg')
        self.image_jpg = makeFileUpload(image_file, 'image/jpeg', 'myportrait.jpg')
        image_file = os.path.join(os.path.dirname(__file__), 'images', 'test.gif')
        self.image_gif = makeFileUpload(image_file, 'image/gif', 'myportrait.gif')

    def test_set_portraits(self):
        mt = getToolByName(self.portal, 'portal_membership')
        mdt = getToolByName(self.portal, 'portal_memberdata')
        mt.changeMemberPortrait(self.image_jpg)
        self.failUnless(default_user in mdt.portraits)
        self.failUnless(default_user in mdt.thumbnails)

        portrait_thumb = mt.getPersonalPortrait()
        from ..tools import PORTRAIT_SIZE, PORTRAIT_THUMBNAIL_SIZE
        self.assertEquals(portrait_thumb.width, PORTRAIT_THUMBNAIL_SIZE[0])
        self.assertEquals(portrait_thumb.height, PORTRAIT_THUMBNAIL_SIZE[1])
        portrait = mt.getPersonalPortrait(thumbnail=False)
        self.assertEquals(portrait.width, PORTRAIT_SIZE[0])
        self.assertEquals(portrait.height, PORTRAIT_SIZE[1])

    def test_change_portraits(self):
        mt = getToolByName(self.portal, 'portal_membership')
        mt.changeMemberPortrait(self.image_jpg)
        portrait = mt.getPersonalPortrait(thumbnail=False)
        old_portrait_size = portrait.get_size()
        portrait = mt.getPersonalPortrait(thumbnail=True)
        old_thumbnail_size = portrait.get_size()

        # Now change the portraits
        mt.changeMemberPortrait(self.image_gif)
        portrait = mt.getPersonalPortrait(thumbnail=False)
        self.failIfEqual(old_portrait_size, portrait.get_size())
        portrait = mt.getPersonalPortrait(thumbnail=True)
        self.failIfEqual(old_thumbnail_size, portrait.get_size())

    def test_delete_portraits(self):
        mt = getToolByName(self.portal, 'portal_membership')
        mdt = getToolByName(self.portal, 'portal_memberdata')
        mt.changeMemberPortrait(self.image_jpg)
        # Now delete the portraits
        mt.deletePersonalPortrait()
        self.failIf(default_user in mdt.portraits)
        self.failIf(default_user in mdt.thumbnails)

    def test_funky_ids(self):
        # Well, let's admit we really do this for the coverage.
        # There is this retarded check in changeMemberPortrait
        # that we copied and have to cover.
        mt = getToolByName(self.portal, 'portal_membership')
        mt.getPersonalPortrait(id='')
        mt.changeMemberPortrait(self.image_gif, id='')


class TestUserSearch(IntranettFunctionalTestCase):

    def test_type(self):
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        self.assertEqual(member.meta_type, 'MemberData')
        self.assertEqual(member.portal_type, 'MemberData')
        self.assertEqual(member.Type(), 'MemberData')

    def test_title(self):
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'John Døe'})
        self.assertEqual(member.Title(), 'John Døe')

    def test_description(self):
        mt = getToolByName(self.portal, 'portal_membership')
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
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'John Døe',
                                    'phone': '12345',
                                    'mobile': '67890',
                                    'position': 'Øngønør',
                                    'department': 'Tøst',
                                    'location': 'Tønsberg',
                                    'email': 'info@jarn.com',
                                    'description': '<p>Kjære Python!</p>'})
        catalog = self.portal.portal_catalog
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
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'description': '<p>Kjære Python!</p>'})
        self.assertEquals(member.SearchableText().strip(), 'Kjære Python!')

    def test_ttw_editing(self):
        browser = self.getBrowser()
        browser.handleErrors = False
        browser.open(self.portal.absolute_url() + '/@@personal-information')
        browser.getControl(name='form.fullname').value = 'John Døe'
        browser.getControl(name='form.email').value = 'test@example.com'
        browser.getControl(name='form.description').value = '<p>Kjære Python!</p>'
        browser.getControl(name='form.location').value = 'Tønsberg'
        browser.getControl(name='form.position').value = 'Øngønør'
        browser.getControl(name='form.department').value = 'Tåst'
        browser.getControl(name='form.actions.save').click()
        self.assert_(browser.url.endswith('@@personal-information'))

    def test_ttw_search(self):
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'fullname': 'John Døe',
                                    'phone': '12345',
                                    'mobile': '67890',
                                    'position': 'Øngønør',
                                    'department': 'Tøst',
                                    'location': 'Tønsberg',
                                    'email': 'info@jarn.com'})
        browser = self.getBrowser()
        browser.open(self.portal.absolute_url())
        browser.getControl(name='SearchableText').value = 'Døe'
        browser.getForm(name='searchform').submit()
        self.failUnless('John Døe' in browser.contents)
        self.failUnless('Øngønør, Tøst' in browser.contents)


class TestDashboard(IntranettTestCase):

    def test_default_dashboard(self):
        from plone.portlets.constants import USER_CATEGORY
        from plone.portlets.interfaces import IPortletManager

        _doAddUser = aq_get(self.portal, 'acl_users')._doAddUser
        _doAddUser('member', 'secret', ['Member'], [])

        prefix = 'plone.dashboard'
        for i in range(1, 5):
            name = prefix + str(i)
            column = queryUtility(IPortletManager, name=name)
            category = column.get(USER_CATEGORY, None)
            manager = category.get('member', {})
            self.assert_(manager == {}, 'Found unexpected portlets in '
                         'dashboard column %s: %s' % (i, manager.keys()))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMemberTools))
    suite.addTest(makeSuite(TestUserdataSchema))
    suite.addTest(makeSuite(TestUserPortraits))
    suite.addTest(makeSuite(TestUserSearch))
    suite.addTest(makeSuite(TestDashboard))
    return suite
