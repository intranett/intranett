from AccessControl import Unauthorized
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestSiteSetup(IntranettTestCase):

    def test_installable_profiles(self):
        from Products.CMFPlone.browser.admin import AddPloneSite
        add = AddPloneSite(self.portal, self.portal.REQUEST)
        profiles = add.profiles()['extensions']
        ids = [p['id'] for p in profiles]
        self.assertEquals(ids, [u'intranett.policy:default'])

    def test_installable_products(self):
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        installable = qi.listInstallableProducts()
        ids = [p['id'] for p in installable]
        self.assertEquals(ids, [])

    def test_PloneFormGen(self):
        tt = getToolByName(self.portal, 'portal_types')
        self.assert_('FormFolder' in tt.keys())
        self.assertEquals(tt['FormFolder'].getIconExprObject(), None)

    def test_site_actions(self):
        self.setRoles('Manager')
        at = getToolByName(self.portal, 'portal_actions')
        actions = at.listActionInfos(object=self.portal,
                                     categories=('site_actions', ))
        ids = set([a['id'] for a in actions])
        self.assertEquals(ids, set(['accessibility']))

    def test_discussion(self):
        # Test that the profile got applied
        cp = getToolByName(self.portal, 'portal_controlpanel')
        actions = set([a.appId for a in cp.listActions()])
        self.assert_('plone.app.discussion' in actions)

    def test_contentrules_disabled(self):
        from plone.contentrules.engine.interfaces import IRuleStorage
        rule = queryUtility(IRuleStorage)
        self.assertFalse(rule.active)

    def test_collection_disabled(self):
        self.loginAsPortalOwner()
        try:
            self.portal.invokeFactory('Topic', 'topic')
        except Unauthorized:
            self.assert_(True)
        else:
            self.assert_(False, 'Unauthorized not raised.') # pragma: no cover

    def test_default_groups(self):
        gtool = getToolByName(self.portal, 'portal_groups')
        self.assertEquals(set(gtool.listGroupIds()),
                          set(['AuthenticatedUsers']))

    def test_portlets_disabled(self):
        self.loginAsPortalOwner()
        from plone.app.portlets.browser import manage
        view = manage.ManageContextualPortlets(self.portal, self.app.REQUEST)

        from plone.portlets.interfaces import IPortletManager
        left = queryUtility(IPortletManager, name='plone.leftcolumn')

        from plone.app.portlets.browser import editmanager
        renderer = editmanager.EditPortletManagerRenderer(
            self.portal, self.app.REQUEST, view, left)

        addable = renderer.addable_portlets()
        ids = [a['addview'].split('/+/')[-1] for a in addable]

        self.assert_('plone.portlet.collection.Collection' not in ids)
        self.assert_('portlets.Calendar' not in ids)
        self.assert_('portlets.Classic' not in ids)
        self.assert_('portlets.Login' not in ids)
        self.assert_('portlets.Review' not in ids)

    def test_content(self):
        # This content is only created in the tests, it's too hard to avoid
        # its creation
        test_content = set(['front-page', 'news', 'events', 'Members'])
        content = set(self.portal.contentIds())
        self.assertEquals(content - test_content, set())

    def test_content_language(self):
        self.assertEquals(self.portal.Language(), 'no')

    def test_language_tool(self):
        tool = getToolByName(self.portal, "portal_languages")
        self.assertEquals(tool.getDefaultLanguage(), 'no')
        self.assertEquals(tool.supported_langs, ['no'])
        self.assertEquals(tool.display_flags, 0)
        self.assertEquals(tool.start_neutral, 0)
        self.assertEquals(tool.use_combined_language_codes, 0)

    def test_locale(self):
        calendar = getToolByName(self.portal, "portal_calendar")
        # Make sure we have Monday
        self.assertEquals(calendar.firstweekday, 0)

    def test_kss_disabled(self):
        kss = getToolByName(self.portal, "portal_kss")
        id_ = '++resource++plone.app.z3cform'
        paz = kss.getResourcesDict()[id_]
        self.assertEquals(paz.getEnabled(), False)

    def test_mail_setup(self):
        name = self.portal.getProperty('email_from_name')
        self.assertNotEquals(name, '')
        address = self.portal.getProperty('email_from_address')
        self.assertNotEquals(address, '')


class TestAdmin(IntranettTestCase):

    def test_overview(self):
        self.loginAsPortalOwner()
        overview = self.app.unrestrictedTraverse('@@plone-overview')
        result = overview()
        self.assert_('View your intranet' in result, result)

    def test_addsite_profiles(self):
        self.loginAsPortalOwner()
        addsite = self.app.unrestrictedTraverse('@@plone-addsite')
        extensions = addsite.profiles()['extensions']
        self.assertEquals(len(extensions), 1)
        profile = extensions[0]
        self.assertEquals(profile['id'], u'intranett.policy:default')

    def test_addsite_call(self):
        self.loginAsPortalOwner()
        addsite = self.app.unrestrictedTraverse('@@plone-addsite')
        result = addsite()
        self.assert_('Create intranet' in result, result)

    def test_addsite_create(self):
        request = self.app.REQUEST
        request.form['form.submitted'] = True
        addsite = queryMultiAdapter(
            (self.app, request), Interface, 'plone-addsite')
        addsite()
        self.assert_('Plone' in self.app.keys())