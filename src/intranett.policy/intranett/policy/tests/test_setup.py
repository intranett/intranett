from AccessControl import Unauthorized
from Acquisition import aq_get
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import Interface

from intranett.policy.tests.base import IntranettTestCase


class TestSiteSetup(IntranettTestCase):

    def test_installable_products(self):
        portal = self.layer['portal']
        qi = getToolByName(portal, 'portal_quickinstaller')
        installable = qi.listInstallableProducts()
        ids = [p['id'] for p in installable]
        self.assertEquals(ids, [])

    def test_PloneFormGen(self):
        portal = self.layer['portal']
        tt = getToolByName(portal, 'portal_types')
        self.assert_('FormFolder' in tt.keys())
        self.assertEquals(tt['FormFolder'].getIconExprObject(), None)

    def test_site_actions(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        at = getToolByName(portal, 'portal_actions')
        actions = at.listActionInfos(object=portal,
                                     categories=('site_actions', ))
        ids = set([a['id'] for a in actions])
        self.assertEquals(ids, set(['accessibility', 'support']))

    def test_clamav(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        self.assertTrue('clamav_properties' in ptool)
        clamav = ptool.clamav_properties
        self.assertEqual(clamav.getProperty('clamav_connection'), 'net')
        self.assertEqual(
            clamav.getProperty('clamav_host'), 'jarn11.gocept.net')

    def test_css_resources(self):
        portal = self.layer['portal']
        css = getToolByName(portal, 'portal_css')
        resources = css.getEvaluatedResources(portal)
        self.assertEqual(len(resources), 4)
        self.assert_(resources[1]._data['id'].startswith('acl_users'))
        self.assert_(resources[2]._data['id'].startswith('IEFixes'))

    def test_kss_resources(self):
        portal = self.layer['portal']
        kss = getToolByName(portal, 'portal_kss')
        self.assertEqual(len(kss.getEvaluatedResources(portal)), 1)

    def test_js_resources(self):
        portal = self.layer['portal']
        js = getToolByName(portal, 'portal_javascripts')
        self.assertEqual(len(js.getEvaluatedResources(portal)), 3)

    def test_discussion(self):
        # Test that the profile got applied
        portal = self.layer['portal']
        cp = getToolByName(portal, 'portal_controlpanel')
        actions = set([a.appId for a in cp.listActions()])
        self.assert_('plone.app.discussion' in actions)

    def test_contentrules_disabled(self):
        from plone.contentrules.engine.interfaces import IRuleStorage
        rule = queryUtility(IRuleStorage)
        self.assertFalse(rule.active)

    def test_collection_disabled(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        try:
            portal.invokeFactory('Topic', 'topic')
        except Unauthorized:
            self.assert_(True)
        else:
            self.assert_(False, 'Unauthorized not raised.') # pragma: no cover

    def test_default_groups(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_groups')
        self.assertEquals(set(gtool.listGroupIds()),
                          set(['AuthenticatedUsers']))

    def test_portlets_disabled(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        from plone.app.portlets.browser import manage
        request = self.layer['request']
        view = manage.ManageContextualPortlets(portal, request)

        from plone.portlets.interfaces import IPortletManager
        left = queryUtility(IPortletManager, name='plone.leftcolumn')

        from plone.app.portlets.browser import editmanager
        renderer = editmanager.EditPortletManagerRenderer(
            portal, request, view, left)

        addable = renderer.addable_portlets()
        ids = [a['addview'].split('/+/')[-1] for a in addable]

        self.assert_('plone.portlet.collection.Collection' not in ids)
        self.assert_('portlets.Calendar' not in ids)
        self.assert_('portlets.Classic' not in ids)
        self.assert_('portlets.Login' not in ids)
        self.assert_('portlets.Review' not in ids)

    def test_siteadmin_portlets(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Member', 'Site Administrator'])
        from plone.app.portlets.browser import manage
        request = self.layer['request']
        view = manage.ManageContextualPortlets(portal, request)

        from plone.portlets.interfaces import IPortletManager
        left = queryUtility(IPortletManager, name='plone.leftcolumn')
        available = set([p.addview for p in left.getAddablePortletTypes()])
        # the ProjectRoomInfo portlet is always assigned to the root and
        # shouldn't be manageable by the customer
        available.remove('intranett.policy.portlets.ProjectRoomInfo')

        from plone.app.portlets.browser import editmanager
        renderer = editmanager.EditPortletManagerRenderer(
            portal, request, view, left)

        addable = renderer.addable_portlets()
        ids = set([a['addview'].split('/+/')[-1] for a in addable])
        # A site admin should be able to add all available portlet types
        self.assertEqual(ids, available)

    def test_content(self):
        # The members folder is always present
        expected = set(['personal', 'users'])
        # This content is only created in tests
        test_content = set(['test-folder'])
        portal = self.layer['portal']
        content = set(portal.contentIds())
        self.assertEquals(content - test_content, expected)

    def test_content_language(self):
        portal = self.layer['portal']
        self.assertEquals(portal.Language(), 'no')

    def test_language_tool(self):
        portal = self.layer['portal']
        tool = getToolByName(portal, "portal_languages")
        self.assertEquals(tool.getDefaultLanguage(), 'no')
        self.assertEquals(tool.supported_langs, ['no'])
        self.assertEquals(tool.display_flags, 0)
        self.assertEquals(tool.start_neutral, 0)
        self.assertEquals(tool.use_combined_language_codes, 0)

    def test_locale(self):
        portal = self.layer['portal']
        calendar = getToolByName(portal, "portal_calendar")
        # Make sure we have Monday
        self.assertEquals(calendar.firstweekday, 0)

    def test_kss_disabled(self):
        portal = self.layer['portal']
        kss = getToolByName(portal, "portal_kss")
        id_ = '++resource++plone.app.z3cform'
        paz = kss.getResourcesDict()[id_]
        self.assertEquals(paz.getEnabled(), False)

    def test_mail_setup(self):
        portal = self.layer['portal']
        name = portal.getProperty('email_from_name')
        self.assertNotEquals(name, '')
        address = portal.getProperty('email_from_address')
        self.assertNotEquals(address, '')
        mailhost = aq_get(portal, 'MailHost')
        self.assertNotEquals(mailhost.smtp_host, '')
        self.assertNotEquals(mailhost.smtp_port, '')

    def test_private_site(self):
        from plone.app.controlpanel import security
        portal = self.layer['portal']
        cp = security.SecurityControlPanelAdapter(portal)
        self.assertEqual(cp.private_site, True)

    def test_secure_cookie(self):
        portal = self.layer['portal']
        acl = aq_get(portal, 'acl_users')
        self.assertEquals(acl.session.getProperty('secure'), True)

    def test_sharing_action_condition(self):
        portal = self.layer['portal']
        action = portal.portal_actions.object.local_roles
        self.assertEqual(action.getProperty('available_expr'),
            "python:getattr(object, 'getProjectRoom', None) is None")

    def test_error_log(self):
        portal = self.layer['portal']
        error_log = aq_get(portal, 'error_log')
        exceptions = error_log.getProperties()['ignored_exceptions']
        self.assertTrue('LinkIntegrityNotificationException' in exceptions)

    def test_tinymce(self):
        from Products.PortalTransforms.interfaces import IPortalTransformsTool
        portal = self.layer['portal']
        tiny = getToolByName(portal, 'portal_tinymce')
        self.assertTrue(tiny.link_using_uids, True)
        transform_utility = queryUtility(IPortalTransformsTool)
        policies = transform_utility.listPolicies()
        policies = [(mimetype, required) for (mimetype, required) in policies
            if mimetype == "text/x-html-safe"]
        self.assertEqual(policies[0][1],
            ('html_to_plone_outputfilters_html', ))


class TestAdmin(IntranettTestCase):

    def test_overview(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        overview = self.layer['app'].unrestrictedTraverse('@@plone-overview')
        result = overview()
        self.assert_('View your intranet' in result, result)

    def test_addsite_call(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        addsite = self.layer['app'].unrestrictedTraverse('@@plone-addsite')
        result = addsite()
        self.assert_('Create intranet' in result, result)

    def test_addsite_create(self):
        from plone.app.testing import login
        from plone.app.testing import SITE_OWNER_NAME
        app = self.layer['app']
        login(app, SITE_OWNER_NAME)
        request = self.layer['request']
        request.form['form.submitted'] = True
        addsite = queryMultiAdapter((app, request), Interface, 'plone-addsite')
        addsite()
        self.assert_('Plone' in app.keys())
