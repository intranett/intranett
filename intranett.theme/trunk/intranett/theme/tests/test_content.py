from plone.app.portlets.portlets import navigation
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from zope.component import getMultiAdapter
from zope.component import getUtility


from intranett.policy.tests.base import IntranettTestCase


class TestContent(IntranettTestCase):

    def test_navigation_portlet(self):
        leftcolumn = '++contextportlets++plone.leftcolumn'
        mapping = self.portal.restrictedTraverse(leftcolumn)
        self.assert_(u'navigation' in mapping.keys())
        nav = mapping[u'navigation']
        self.assertEquals(nav.topLevel, 1)
        self.assertEquals(nav.currentFolderOnly, True)

    def test_navigation_portlet_template(self):
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=context)
        assignment = navigation.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment),
            IPortletRenderer)

        html = renderer.render()
        # We'd really like to test that we use our own template here
        self.assert_('<dl class="portlet portletNavigationTree">' in html)
