from zope.component import queryUtility

from intranett.policy.tests.base import IntranettTestCase


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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUserdataSchema))
    return suite
