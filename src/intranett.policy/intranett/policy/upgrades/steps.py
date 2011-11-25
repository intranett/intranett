from Acquisition import aq_get
from plone.app.upgrade.utils import loadMigrationProfile
from plutonian.gs import upgrade_to
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager
from zope.component import queryUtility
from zope.i18n import translate


@upgrade_to(7)
def update_caching_config(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('plone.app.registry', ))


@upgrade_to(8)
def migrate_portraits(context):
    from intranett.policy.tools import Portrait

    def migrate_image(container, id):
        image = container[id]
        # handle both str and Pdata
        data = str(image.data)
        portrait = Portrait(id=id, file=data, title='')
        portrait.manage_permission('View', ['Authenticated', 'Manager'],
            acquire=False)
        container._delObject(id)
        container._setObject(id, portrait)

    data = getToolByName(context, 'portal_memberdata')
    for k in data.portraits.keys():
        migrate_image(data.portraits, k)
    for k in data.thumbnails.keys():
        migrate_image(data.thumbnails, k)


@upgrade_to(9)
def disable_webstats_js(context):
    ptool = getToolByName(context, 'portal_properties')
    sprops = ptool.site_properties
    sprops.webstats_js = ''


@upgrade_to(10)
def remove_unused_frontpage_portlets(context):
    from plone.portlets.interfaces import IPortletManager
    sm = getSiteManager()
    names = ('frontpage.portlets.left', 'frontpage.portlets.central',
        'frontpage.bottom')
    for name in names:
        sm.unregisterUtility(provided=IPortletManager, name=name)


@upgrade_to(11)
def add_site_administrator(context):
    url_tool = getToolByName(context, 'portal_url')
    site = url_tool.getPortalObject()
    existing_roles = set(getattr(site, '__ac_roles__', []))
    existing_roles.add('Site Administrator')
    site.__ac_roles__ = tuple(existing_roles)
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('rolemap', 'actions'))


@upgrade_to(12)
def allow_site_admin_to_edit_frontpage(context):
    from plone.portlets.interfaces import IPortletType
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('rolemap', ))
    fti = getToolByName(context, 'portal_types')['Plone Site']
    edit_action = [a for a in fti.listActions() if a.id == 'edit-frontpage']
    edit_action[0].permissions = (u'Portlets: Manage portlets', )
    coll_id = u'plone.portlet.collection.Collection'
    coll = queryUtility(IPortletType, name=coll_id)
    coll.for_ = []


@upgrade_to(13)
def allow_member_to_edit_personal_portlets(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('rolemap', ))


@upgrade_to(14)
def add_frontpage_cacherule(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('plone.app.registry', ))


@upgrade_to(15)
def change_frontpage_portlets(context):
    from plone.portlets.interfaces import IPortletManager
    sm = getSiteManager()
    sm.unregisterUtility(provided=IPortletManager, name='frontpage.highlight')
    loadMigrationProfile(context, 'profile-intranett.theme:default',
        steps=('portlets', ))


@upgrade_to(16)
def allow_siteadmin_to_edit_content(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('rolemap', 'workflow', ))


@upgrade_to(17)
def install_highlight_portlets(context):
    pass


@upgrade_to(18)
def deactivate_collective_flag(context):
    catalog = getToolByName(context, 'portal_catalog')
    if 'flaggedobject' in catalog.indexes():
        catalog.delIndex('flaggedobject')
    atct = getToolByName(context, 'portal_atct')
    atct.removeIndex('flaggedobject')


@upgrade_to(19)
def update_discussion_10(context):
    loadMigrationProfile(context, 'profile-plone.app.discussion:default',
        steps=('actions', 'plone.app.registry', 'rolemap', ))
    actions = getToolByName(context, 'portal_actions')
    user_category = actions.user
    review = user_category['review-comments']
    review.visible = False
    if 'manage_users' in user_category: # pragma: no cover
        pos = user_category.getObjectPosition('manage_users')
        user_category.moveObjectToPosition('review-comments', pos)
    aitool = getToolByName(context, 'portal_actionicons')
    ids = [a._action_id for a in aitool.listActionIcons()]
    if 'discussion' in ids:
        aitool.removeActionIcon('controlpanel', 'discussion')
    control = getToolByName(context, 'portal_controlpanel')
    disc = [a for a in control.listActions() if a.id == 'discussion'][0]
    disc.category = 'Plone'


@upgrade_to(20)
def update_clamav_settings(context):
    ptool = getToolByName(context, 'portal_properties')
    clamav = ptool.clamav_properties
    clamav.clamav_connection = 'net'
    clamav.clamav_host = 'jarn11.gocept.net'
    clamav.clamav_port = '3310'
    clamav.clamav_timeout = 120
    # return to default
    clamav.clamav_socket = '/var/run/clamd'


@upgrade_to(21)
def install_users_folder(context):
    # Remove the employee-listing action
    atool = getToolByName(context, 'portal_actions')
    if 'employee-listing' in atool.portal_tabs:
        atool.portal_tabs._delObject('employee-listing')
    # Add the MembersFolder portal type
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('typeinfo', 'factorytool', 'propertiestool'))
    # Add the users folder
    from intranett.policy.config import MEMBERS_FOLDER_ID
    from intranett.policy.setuphandlers import setup_members_folder
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if MEMBERS_FOLDER_ID not in portal:
        setup_members_folder(portal)
    # Remove orphaned member data records
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(dict(portal_type='MemberData'))
    for brain in brains:
        catalog.uncatalog_object(brain.getPath())
    # Reindex member data
    mt = getToolByName(context, 'portal_membership')
    for member in mt.listMembers():
        member.notifyModified()


@upgrade_to(22)
def enable_secure_cookies(context):
    from intranett.policy.setuphandlers import enable_secure_cookies
    enable_secure_cookies(context)


@upgrade_to(23)
def update_strong_caching_maxage(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('plone.app.registry', ))


@upgrade_to(24)
def update_strong_caching_maxage2(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('plone.app.registry', ))


@upgrade_to(25)
def update_users_folder_title(context):
    url_tool = getToolByName(context, 'portal_url')
    site = url_tool.getPortalObject()
    fti = getToolByName(site, 'portal_types')['MembersFolder']
    if 'users' in site:
        title = translate(fti.Title(), target_language=site.Language())
        site['users'].setTitle(title)
        site['users'].reindexObject()


@upgrade_to(26)
def ignore_linkintegrity_exceptions(context):
    from intranett.policy.setuphandlers import ignore_link_integrity_exceptions
    site = getToolByName(context, 'portal_url').getPortalObject()
    ignore_link_integrity_exceptions(site)


@upgrade_to(27)
def add_help_site_action(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('actions', ))


@upgrade_to(28)
def enable_link_by_uid(context):
    from intranett.policy.setuphandlers import enable_link_by_uid
    site = getToolByName(context, 'portal_url').getPortalObject()
    enable_link_by_uid(site)


@upgrade_to(29)
def cleanup_plone41(context):
    url_tool = getToolByName(context, 'portal_url')
    site = url_tool.getPortalObject()
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('languagetool', 'plone.app.registry', ))
    loadMigrationProfile(context, 'profile-plone.app.jquerytools:default',
        steps=('cssregistry', 'jsregistry', ))
    # unregister persistent steps
    registry = context.getImportStepRegistry()
    for step in ('mimetypes-registry-various', 'plonepas'):
        if step in registry._registered:
            registry.unregisterStep(step)
    context._p_changed = True
    # remove `Site Administrators` group
    gtool = getToolByName(context, 'portal_groups')
    ids = gtool.getGroupIds()
    if 'Site Administrators' in ids:
        gtool.removeGroups(['Site Administrators'])
    # reorder new external_login properties
    ptool = getToolByName(context, 'portal_properties')
    sprops = ptool.site_properties
    ids = sprops.propertyIds()
    if 'external_login_iframe' not in ids:
        sprops._setProperty('external_login_iframe', False, type='boolean')
    _properties = []
    use_folder_tabs = None
    for p in sprops._properties:
        if p['id'] == 'use_folder_tabs':
            use_folder_tabs = p
        else:
            _properties.append(p)
    _properties.append(use_folder_tabs)
    sprops._properties = tuple(_properties)
    sprops._p_changed = True
    # take care of skin layers
    skins = getToolByName(context, 'portal_skins')
    for key, value in skins.selections.items():
        new = value.replace('LanguageTool,', '')
        new = new.replace('PloneFormGen,tinymce,referencebrowser,',
            'PloneFormGen,referencebrowser,tinymce,LanguageTool,')
        skins.selections[key] = new
    # UID index only supports string criteria
    portal_atct = getToolByName(context, 'portal_atct')
    portal_atct.topic_indexes['UID'].criteria = ('ATSimpleStringCriterion', )
    # CSS
    css = getToolByName(context, 'portal_css')
    css.moveResourceAfter(
        '++resource++plone.app.discussion.stylesheets/discussion.css',
        'member.css')
    css.moveResourceAfter(
        '++resource++plone.app.jquerytools.dateinput.css',
        '++resource++plone.app.jquerytools.overlays.css')
    res = css.getResource('++resource++plone.app.jquerytools.overlays.css')
    res.setEnabled(False)
    # actions
    actions = getToolByName(context, 'portal_actions')
    if 'plone_setup' in actions.user:
        del actions.user['plone_setup']
    # handle security
    loadMigrationProfile(context, 'profile-Products.CMFPlone:plone',
        steps=('rolemap', 'workflow', ))
    loadMigrationProfile(context, 'profile-plone.app.discussion:default',
        steps=('workflow', ))
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('rolemap', 'workflow', ))
    from intranett.policy.setuphandlers import disallow_sendto
    from intranett.policy.setuphandlers import restrict_siteadmin
    disallow_sendto(site)
    restrict_siteadmin(site)
    # handle kupu
    try:
        delattr(site, '_Kupu__Manage_libraries_Permission')
        delattr(site, '_Kupu__Query_libraries_Permission')
    except AttributeError:
        pass
    from plone.app.upgrade.v41.alphas import update_role_mappings
    update_role_mappings(context)


@upgrade_to(30)
def protect_images(context):
    from plone.app.workflow.remap import remap_workflow
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('workflow', 'plone.app.registry'))
    url_tool = getToolByName(context, 'portal_url')
    site = url_tool.getPortalObject()
    remap_workflow(site,
                   type_ids=('Discussion Item', 'File', 'Image'),
                   chain=('one_state_intranett_workflow', ))


@upgrade_to(31)
def site_admins_can_review_comments(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('rolemap',))


@upgrade_to(32)
def ext_links_in_new_window(context):
    from intranett.policy.setuphandlers import open_ext_links_in_new_window
    ptool = getToolByName(context, 'portal_properties')
    ptool.site_properties.external_links_open_new_window = 'true'
    open_ext_links_in_new_window(context)


@upgrade_to(33)
def add_personal_folder(context):
    from intranett.policy.config import PERSONAL_FOLDER_ID
    from intranett.policy.setuphandlers import setup_personal_folder
    from intranett.policy.subscribers.users import create_personal_folder
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if PERSONAL_FOLDER_ID not in portal:
        setup_personal_folder(portal)
        # create personal folders for existing users
        acl_users = aq_get(portal, 'acl_users')
        user_ids = [a for a in acl_users.source_users.listUserIds()]
        for user_id in user_ids:
            create_personal_folder(portal, user_id)
    actions = getToolByName(context, 'portal_actions')
    user_category = actions.user
    if 'manage_users' in user_category: # pragma: no cover
        del user_category['manage_users']


@upgrade_to(34)
def remove_crappy_portlets(context):
    # Remove portlets -- the code tried to remove named portlet managers :(
    # Remove CSS/JS
    prefix = '++resource++plone.formwidget.autocomplete/jquery.autocomplete'
    css = getToolByName(context, 'portal_css')
    ids = css.getResourcesDict().keys()
    css_id = prefix + '.css'
    if css_id in ids: # pragma: no cover
        css.unregisterResource(css_id)
        css.cookResources()
    js = getToolByName(context, 'portal_javascripts')
    ids = js.getResourcesDict().keys()
    js_id = prefix + '.min.js'
    if js_id in ids: # pragma: no cover
        js.unregisterResource(js_id)
        js.cookResources()


@upgrade_to(35)
def install_project_rooms(context):
    from plone.app.workflow.remap import remap_workflow
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('actions', 'catalog', 'factorytool', 'plone.app.registry',
               'portlets', 'typeinfo', 'workflow', ))
    url_tool = getToolByName(context, 'portal_url')
    site = url_tool.getPortalObject()
    remap_workflow(site,
                   type_ids=('File', 'Image'),
                   chain=('two_state_intranett_workflow', ))


@upgrade_to(36)
def fix_small_problems(context):
    # add type to factory tool
    ftool = getToolByName(context, 'portal_factory')
    types = set(ftool.getFactoryTypes().keys())
    types.add('ProjectRoom')
    ftool.manage_setPortalFactoryTypes(listOfTypeIds=list(types))
    # remove crappy portlets
    from plone.portlets.interfaces import IPortletType
    sm = getSiteManager()
    names = ('intranett.policy.portlets.NewsHighlight',
             'intranett.policy.portlets.EventHighlight',
             'intranett.policy.portlets.ContentHighlight')
    for name in names:
        sm.unregisterUtility(provided=IPortletType, name=name)


@upgrade_to(37)
def fix_resource_compression_settings(context):
    loadMigrationProfile(context, 'profile-intranett.theme:default',
        steps=('jsregistry', ))
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('jsregistry', ))


@upgrade_to(38)
def counter_plone_js_upgrade(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('jsregistry', ))


@upgrade_to(39)
def enable_session_refresh(context):
    from intranett.policy.setuphandlers import enable_secure_cookies
    enable_secure_cookies(context)
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('cssregistry', ))


@upgrade_to(40)
def set_site_title(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
    steps=('properties', ))


@upgrade_to(41)
def install_quickupload(context):
    loadMigrationProfile(context, 'profile-collective.quickupload:default')
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('cssregistry', 'jsregistry', 'propertiestool'))
    from intranett.policy.setuphandlers import setup_quickupload
    setup_quickupload(context)


@upgrade_to(42)
def install_amberjack(context):
    loadMigrationProfile(context, 'profile-intranett.tour:default')
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('cssregistry', 'jsregistry', ))
    from intranett.policy.setuphandlers import setup_amberjack
    url_tool = getToolByName(context, 'portal_url')
    site = url_tool.getPortalObject()
    setup_amberjack(site)


@upgrade_to(43)
def remove_kss(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('jsregistry', ))


@upgrade_to(44)
def quickupload_in_personal_folder(context):
    from plone.portlets.interfaces import IPortletType
    from intranett.policy.config import PERSONAL_FOLDER_ID
    from intranett.policy import IntranettMessageFactory as _
    url_tool = getToolByName(context, 'portal_url')
    portal = url_tool.getPortalObject()
    portlet = queryUtility(IPortletType,
         name='collective.quickupload.QuickUploadPortlet')
    personal = portal[PERSONAL_FOLDER_ID]
    mapping = personal.restrictedTraverse('++contextportlets++plone.leftcolumn')
    addview = mapping.restrictedTraverse('+/' + portlet.addview)
    quick_title = _(u'Quick upload')
    addview.createAndAdd(data={'header':
        translate(quick_title, target_language=portal.Language())})


@upgrade_to(45)
def add_invite_portlet(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('portlets', 'skins', 'toolset', 'rolemap'))


@upgrade_to(46)
def remove_unused_workflows(context):
    from intranett.policy.setuphandlers import remove_unused_workflows
    remove_unused_workflows(context)


@upgrade_to(47)
def install_xmpp(context):
    loadMigrationProfile(context, 'profile-jarn.xmpp.core:default')
    loadMigrationProfile(context, 'profile-jarn.xmpp.collaboration:default')
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('cssregistry', 'kssregistry', ))
