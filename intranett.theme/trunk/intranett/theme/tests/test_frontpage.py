from plone.portlets.interfaces import IPortletManager
from zope.component import getSiteManager

from intranett.policy.tests.base import IntranettTestCase


class TestFrontpage(IntranettTestCase):

    def test_columns_class_default(self):
        view = self.portal.unrestrictedTraverse('@@frontpage_view')
        self.assertEquals(view.columns_class(), 'width-16')

    def test_columns_class_no_portlets(self):
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.left')
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.central')
        sm.unregisterUtility(provided=IPortletManager,
                             name=u'frontpage.portlets.right')

        view = self.portal.unrestrictedTraverse('@@frontpage_view')
        self.assertEquals(view.columns_class(), False)
