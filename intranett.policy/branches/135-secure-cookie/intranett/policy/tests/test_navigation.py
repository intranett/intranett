from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from intranett.policy.tests.base import IntranettTestCase


class TestNavigation(IntranettTestCase):

    def _make_one(self):
        portal = self.layer['portal']
        request = self.layer['request']
        portal_tabs_view = getMultiAdapter((portal, request),
                                           name='portal_tabs_view')
        return portal_tabs_view.topLevelTabs()

    def test_default(self):
        tabs = self._make_one()
        self.assert_(len(tabs) > 0)
        self.assertEquals(tabs[-1]['id'], 'employee-listing')

    def test_published_folders(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        wftool = getToolByName(portal, 'portal_workflow')
        portal.invokeFactory('Folder', 'f1')
        portal.invokeFactory('Folder', 'f2')
        wftool.doActionFor(portal.f1, 'publish')
        wftool.doActionFor(portal.f2, 'publish')
        setRoles(portal, TEST_USER_ID, ['Member'])

        tabs = self._make_one()
        self.assert_(len(tabs) > 1)
        self.assertEquals(tabs[-1]['id'], 'employee-listing')
