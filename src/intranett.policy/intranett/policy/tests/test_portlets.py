from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility, getMultiAdapter

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.browser.portlets import newshighlight


class TestNewsHighlightPortlet(IntranettTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.layer['portal']
        request = request or context.REQUEST
        view = view or context.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=context)
        assignment = assignment or newshighlight.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_news_items(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        wt = getToolByName(portal, 'portal_workflow')

        yesterday = DateTime() - 1
        day_before_yesterday = yesterday - 1

        portal.invokeFactory('News Item', 'wedding',
                             title='A wedding')
        portal['wedding'].setModificationDate(day_before_yesterday)
        wt.doActionFor(portal['wedding'], 'publish')

        portal.invokeFactory('News Item', 'funeral',
                             title='A funeral')
        portal['funeral'].setModificationDate(yesterday)
        wt.doActionFor(portal['funeral'], 'publish')

        assignment = newshighlight.Assignment(
            portletTitle="News",
            source='last')
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        item = r.item
        self.assertEqual(item.Title, 'A funeral')
        output = r.render()
        self.assertTrue('News' in output)
        self.assertTrue('A funeral' in output)

        assignment = newshighlight.Assignment(
            portletTitle="News",
            source='before-last')
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        item = r.item
        self.assertEqual(item.Title, 'A wedding')
        output = r.render()
        self.assertTrue('News' in output)
        self.assertTrue('A wedding' in output)
