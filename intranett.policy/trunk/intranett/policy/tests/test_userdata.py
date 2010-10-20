from Acquisition import aq_get
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from intranett.policy.tests.base import IntranettTestCase
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
        self.failUnless('department' in schema)
        self.failUnless('phone' in schema)
        self.failUnless('mobile' in schema)

    def test_memberinfo(self):
        mt = getToolByName(self.portal, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties({'phone': '12345',
                                    'mobile': '67890',
                                    'department': 'it',
                                    'email': 'info@jarn.com'})
        info = mt.getMemberInfo()
        self.assertEquals(info['phone'], '12345')
        self.assertEquals(info['mobile'], '67890')
        self.assertEquals(info['department'], 'it')
        self.assertEquals(info['email'], 'info@jarn.com')

        info = mt.getMemberInfo(memberId='foo')
        self.failUnless(info is None)

    def test_userpanel(self):
        from ..userdataschema import ICustomUserDataSchema
        panel = ICustomUserDataSchema(self.portal)
        self.assertEquals(panel.department, '')
        panel.department = 'it'
        self.assertEquals(panel.department, 'it')
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
    suite.addTest(makeSuite(TestDashboard))
    return suite
