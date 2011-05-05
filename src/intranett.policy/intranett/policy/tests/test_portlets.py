from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
import transaction
from zope.component import getUtility, getMultiAdapter

from intranett.policy.browser.portlets import contenthighlight
from intranett.policy.browser.portlets import eventhighlight
from intranett.policy.browser.portlets import newshighlight
from intranett.policy.browser.portlets import workspaceinfo
from intranett.policy.browser.sources import DocumentSourceBinder
from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.base import get_browser


class TestPortlets(IntranettTestCase):

    def test_navigation_portlet(self):
        portal = self.layer['portal']
        leftcolumn = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(leftcolumn)
        self.assert_(u'navigation' in mapping.keys())
        nav = mapping[u'navigation']
        self.assertEquals(nav.topLevel, 1)
        self.assertEquals(nav.currentFolderOnly, True)


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
        initial = len(mapping)
        addview.createAndAdd(
            data={'portletTitle': 'News Highlight', 'source': 'last'})
        self.assertEquals(len(mapping), 1+initial)
        assignment_types = set(assignment.__class__ for assignment in mapping.values())
        self.assertIn(newshighlight.Assignment, assignment_types)


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
                             startDate=tomorrow, endDate=tomorrow + 1)
        wt.doActionFor(portal['wedding'], 'publish')
        portal.invokeFactory('Event', 'funeral',
                             title='A funeral',
                             startDate=in_a_month, endDate=in_a_month + 1)
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
        initial = len(mapping)
        addview.createAndAdd(
            data={'portletTitle': 'Event Highlight'})
        self.assertEquals(len(mapping), 1+initial)
        assignment_types = set(assignment.__class__ for assignment in mapping.values())
        self.assertIn(eventhighlight.Assignment, assignment_types)


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

        # Let's use a non-existing item
        assignment = contenthighlight.Assignment(
            portletTitle="Highlighted",
            item='i_do_not_exist')
        r = self.renderer(assignment=assignment)
        r = r.__of__(portal)
        r.update()
        self.assertEqual(r.item(), None)
        output = r.render()
        self.assertTrue('Highlighted' not in output)

    def test_invoke_add_view(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portlet = getUtility(IPortletType,
            name='intranett.policy.portlets.ContentHighlight')
        mapping = portal.restrictedTraverse(
            '++contextportlets++plone.rightcolumn')
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        initial = len(mapping)
        addview.createAndAdd(
            data={'portletTitle': 'Content Highlight', 'item': 'xxx'})
        self.assertEquals(len(mapping), 1+initial)
        assignment_types = set(assignment.__class__ for assignment in mapping.values())
        self.assertIn(contenthighlight.Assignment, assignment_types)

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

        # Containment
        self.assertTrue(uid in query_source)
        # Length
        self.assertEqual(len(query_source), 1)
        # Iterator
        self.assertTrue(len([x for x in query_source]), 1)
    

class TestWorkspaceStatePortlet(IntranettTestCase):

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

    def test_private_space(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        workspace_id = portal.invokeFactory('TeamWorkspace', 'workspace',
                             title='First Space')
        workspace = portal[workspace_id]

        assignment = workspaceinfo.Assignment()
        r = self.renderer(context=workspace, assignment=assignment)
        r = r.__of__(workspace)
        r.update()

        self.assertEqual(r.state, 'private')
        self.assertEqual(r.members, ('', )) # only the admin

    def test_public_space(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        wt = getToolByName(portal, 'portal_workflow')
        workspace_id = portal.invokeFactory('TeamWorkspace', 'workspace',
                             title='First Space')
        workspace = portal[workspace_id]
        wt.doActionFor(workspace, "publish")

        assignment = workspaceinfo.Assignment()
        r = self.renderer(context=workspace, assignment=assignment)
        r = r.__of__(workspace)
        r.update()

        self.assertEqual(r.state, 'public')
        self.assertEqual(r.members, ("", )) # only the admin

    def test_member_fullname_shown(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        wt = getToolByName(portal, 'portal_workflow')
        workspace_id = portal.invokeFactory('TeamWorkspace', 'workspace',
                             title='First Space')
        workspace = portal[workspace_id]
        workspace.members = (TEST_USER_ID, )
        wt.doActionFor(workspace, "publish")

        assignment = workspaceinfo.Assignment()
        r = self.renderer(context=workspace, assignment=assignment)
        r = r.__of__(workspace)
        r.update()

        self.assertEqual(r.state, 'public')
        self.assertEqual(r.members, ("", )) # admin and test_user_1_ have no name

    def test_outside_workspace_no_portlet_rendered(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])

        assignment = workspaceinfo.Assignment()
        r = self.renderer(context=portal, assignment=assignment)
        r = r.__of__(portal)
        r.update()

        self.assertFalse(r.available)
        output = r.render()
        self.assertEqual(output.strip(), "")
    

class TestZ3cBase(IntranettFunctionalTestCase):

    def test_add_edit_forms(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        wt = getToolByName(portal, 'portal_workflow')
        portal.invokeFactory('Document', 'adoc',
                             title='A document')
        wt.doActionFor(portal['adoc'], 'publish')
        title = portal['adoc'].Title()
        transaction.commit()
        browser = get_browser(self.layer['app'], loggedIn=True)
        url = portal.absolute_url() + \
            '/++contextportlets++plone.leftcolumn/+/' + \
            'intranett.policy.portlets.ContentHighlight'
        # Missing input
        browser.open(url)
        browser.getControl(name='form.buttons.add').click()
        self.assertEqual(browser.url, url)
        self.assertTrue('Required input is missing.' in browser.contents)
        # Add
        browser.getControl(name='form.widgets.portletTitle').value = 'A title'
        browser.getControl(
            name="form.widgets.item.widgets.query").value = title
        browser.getControl(name='form.buttons.add').click()
        browser.getControl(name='form.widgets.item:list').value = [title]
        browser.getControl(name='form.buttons.add').click()
        self.assertEqual(browser.url, 'http://nohost/plone/@@manage-portlets')
        # Cancel add
        browser.open(url)
        browser.getControl(name='form.buttons.cancel_add').click()
        self.assertEqual(browser.url, 'http://nohost/plone/@@manage-portlets')

        url = portal.absolute_url() + \
            '/++contextportlets++plone.leftcolumn/' + \
            'content-highlight/edit'
        # Missing input
        browser.open(url)
        browser.getControl(name='form.widgets.portletTitle').value = ''
        browser.getControl(name='form.buttons.apply').click()
        self.assertEqual(browser.url, url)
        self.assertTrue('Required input is missing.' in browser.contents)
        # Edit without changes
        browser.getControl(name='form.widgets.portletTitle').value = 'A title'
        browser.getControl(name='form.buttons.apply').click()
        self.assertEqual(browser.url, 'http://nohost/plone/@@manage-portlets')
        # Edit with changes
        browser.open(url)
        browser.getControl(name='form.widgets.portletTitle').value = 'Title 2'
        browser.getControl(name='form.buttons.apply').click()
        self.assertEqual(browser.url, 'http://nohost/plone/@@manage-portlets')
        # Cancel edit
        browser.open(url)
        browser.getControl(name='form.buttons.cancel_add').click()
        self.assertEqual(browser.url, 'http://nohost/plone/@@manage-portlets')
