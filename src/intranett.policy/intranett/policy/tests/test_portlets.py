from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility, getMultiAdapter

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.browser.portlets import eventhighlight
from intranett.policy.browser.portlets import newshighlight
from intranett.policy.browser.portlets import contenthighlight
from intranett.policy.browser.sources import DocumentSourceBinder


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

        # No news items
        assignment = newshighlight.Assignment(
            portletTitle='News',
            source='last')
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        self.assertEqual(r.item(), None)
        output = r.render()
        self.assertTrue('News' not in output)

        yesterday = DateTime() - 1
        day_before_yesterday = yesterday - 1

        # One news item.
        portal.invokeFactory('News Item', 'wedding',
                             title='A wedding')
        portal['wedding'].setEffectiveDate(day_before_yesterday)
        wt.doActionFor(portal['wedding'], 'publish')

        # We want the one before last, which does not exist.
        assignment = newshighlight.Assignment(
            portletTitle="News",
            source='before-last')
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        self.assertEqual(r.item(), None)
        output = r.render()
        self.assertTrue('News' not in output)

        # Two news items.
        portal.invokeFactory('News Item', 'funeral',
                             title='A funeral')
        portal['funeral'].setEffectiveDate(yesterday)
        wt.doActionFor(portal['funeral'], 'publish')

        # Show the last
        assignment = newshighlight.Assignment(
            portletTitle='News',
            source='last')
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        self.assertEqual(r.item().Title, 'A funeral')
        output = r.render()
        self.assertTrue('News' in output)
        self.assertTrue('A funeral' in output)

        # Show the one before last.
        assignment = newshighlight.Assignment(
            portletTitle="News",
            source='before-last')
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        self.assertEqual(r.item().Title, 'A wedding')
        output = r.render()
        self.assertTrue('News' in output)
        self.assertTrue('A wedding' in output)

    def test_invoke_add_view(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portlet = getUtility(IPortletType,
            name='intranett.policy.portlets.NewsHighlight')
        mapping = portal.restrictedTraverse(
            '++contextportlets++plone.rightcolumn')
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(
            data={'portletTitle': 'News Highlight', 'source': 'last'})
        self.assertEquals(len(mapping), 1)
        self.failUnless(
            isinstance(mapping.values()[0], newshighlight.Assignment))


class TestEventHighlightPortlet(IntranettTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.layer['portal']
        request = request or context.REQUEST
        view = view or context.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=context)
        assignment = assignment or eventhighlight.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_upcoming_event(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        wt = getToolByName(portal, 'portal_workflow')

        # No event
        assignment = eventhighlight.Assignment(
            portletTitle="Event")
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        self.assertEqual(r.item(), None)
        output = r.render()
        self.assertTrue('Event' not in output)

        # Add two events, show the last.
        tomorrow = DateTime() + 1
        in_a_month = tomorrow + 30
        portal.invokeFactory('Event', 'wedding',
                             title='A wedding',
                             startDate=tomorrow, endDate=tomorrow+1)
        wt.doActionFor(portal['wedding'], 'publish')
        portal.invokeFactory('Event', 'funeral',
                             title='A funeral',
                             startDate=in_a_month, endDate=in_a_month+1)
        wt.doActionFor(portal['funeral'], 'publish')

        assignment = eventhighlight.Assignment(
            portletTitle="Event")
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        self.assertEqual(r.item().Title, 'A wedding')
        output = r.render()
        self.assertTrue('Event' in output)
        self.assertTrue('A wedding' in output)

    def test_invoke_add_view(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portlet = getUtility(IPortletType,
            name='intranett.policy.portlets.EventHighlight')
        mapping = portal.restrictedTraverse(
            '++contextportlets++plone.rightcolumn')
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(
            data={'portletTitle': 'Event Highlight'})
        self.assertEquals(len(mapping), 1)
        self.failUnless(
            isinstance(mapping.values()[0], eventhighlight.Assignment))


class TestContentHighlightPortlet(IntranettTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.layer['portal']
        request = request or context.REQUEST
        view = view or context.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=context)
        assignment = assignment or contenthighlight.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_highighted_content(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        wt = getToolByName(portal, 'portal_workflow')
        portal.invokeFactory('Document', 'highlighted',
                             title='A highlighted document')
        wt.doActionFor(portal['highlighted'], 'publish')

        uid = portal['highlighted'].UID()
        assignment = contenthighlight.Assignment(
            portletTitle="Highlighted",
            item=uid)
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()

        self.assertEqual(r.item().Title, 'A highlighted document')
        output = r.render()
        self.assertTrue('Highlighted' in output)
        self.assertTrue('A highlighted document' in output)

    def test_document_source(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        wt = getToolByName(portal, 'portal_workflow')
        portal.invokeFactory('Document', 'adoc',
                             title='A document')
        wt.doActionFor(portal['adoc'], 'publish')
        uid = portal['adoc'].UID()
        title = portal['adoc'].Title()

        binder = DocumentSourceBinder()
        query_source = binder(portal)
        term = query_source.getTerm(uid)
        self.assertEqual(term.value, uid)
        self.assertEqual(term.token, title)
        term = query_source.getTermByToken(title)
        self.assertEqual(term.value, uid)
        self.assertEqual(term.token, title)

        search_result = query_source.search('a doc')
        self.assertNotEqual(search_result, [])
        term = search_result[0]
        self.assertEqual(term.value, uid)
        self.assertEqual(term.token, title)
