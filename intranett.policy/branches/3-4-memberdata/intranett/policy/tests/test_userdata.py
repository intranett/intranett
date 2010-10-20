from Acquisition import aq_get
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from intranett.policy.tests.base import IntranettTestCase


class TestMembershipTool(IntranettTestCase):

    def test_tool_registered(self):
        #Check we can get the tool by name
        from ..membershiptool import MembershipTool
        tool = getToolByName(self.portal, 'portal_membership')
        self.failUnless(isinstance(tool, MembershipTool))
        #Check we can get the tool by PlonePAS interface
        from Products.PlonePAS.interfaces.membership import IMembershipTool
        mt = queryUtility(IMembershipTool)
        self.failIf(mt is None)
        self.failUnless(isinstance(mt, MembershipTool))
        #Check we can get the tool by CMFCore interface
        from Products.CMFCore.interfaces import IMembershipTool
        mt2 = queryUtility(IMembershipTool)
        self.failUnless(mt == mt2)


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
    suite.addTest(makeSuite(TestUserdataSchema))
    suite.addTest(makeSuite(TestMembershipTool))
    suite.addTest(makeSuite(TestDashboard))
    return suite
