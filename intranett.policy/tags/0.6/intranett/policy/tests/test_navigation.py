from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from intranett.policy.tests.base import IntranettTestCase


class TestNavigation(IntranettTestCase):

    def _make_one(self):
        portal_tabs_view = getMultiAdapter((self.portal, self.app.REQUEST),
                                           name='portal_tabs_view')
        return portal_tabs_view.topLevelTabs()

    def test_default(self):
        tabs = self._make_one()
        self.assert_(len(tabs) > 0)
        self.assertEquals(tabs[-1]['id'], 'employee-listing')

    def test_published_folders(self):
        self.setRoles(('Manager', ))
        wftool = getToolByName(self.portal, 'portal_workflow')
        self.portal.invokeFactory('Folder', 'f1')
        self.portal.invokeFactory('Folder', 'f2')
        wftool.doActionFor(self.portal.f1, 'publish')
        wftool.doActionFor(self.portal.f2, 'publish')
        self.setRoles(('Member', ))

        tabs = self._make_one()
        self.assert_(len(tabs) > 1)
        self.assertEquals(tabs[-1]['id'], 'employee-listing')
