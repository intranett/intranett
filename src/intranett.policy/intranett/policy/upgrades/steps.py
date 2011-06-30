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
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('portlets', ))
    # Add CSS/JS
    prefix = '++resource++plone.formwidget.autocomplete/jquery.autocomplete'
    css = getToolByName(context, 'portal_css')
    ids = css.getResourcesDict().keys()
    css_id = prefix + '.css'
    if css_id not in ids:
        css.registerStylesheet(css_id)
        css.moveResourceAfter(css_id, 'RTL.css')
    js = getToolByName(context, 'portal_javascripts')
    ids = js.getResourcesDict().keys()
    js_id = prefix + '.min.js'
    if js_id not in ids:
        js.registerScript(js_id)
        js.moveResourceBefore(js_id, 'tiny_mce.js')


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
    acl = aq_get(context, 'acl_users')
    acl.session._updateProperty('secure', True)


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
        '++resource++plone.formwidget.autocomplete/jquery.autocomplete.css')
    css.moveResourceAfter(
        '++resource++plone.app.jquerytools.dateinput.css',
        '++resource++plone.app.jquerytools.overlays.css')
    res = css.getResource('++resource++plone.app.jquerytools.overlays.css')
    res.setEnabled(False)
    # actions
    actions = getToolByName(context, 'portal_actions')
    if 'plone_setup' in actions.user:
        del actions.user['plone_setup']
    # XXX this can go once p.a.upgrade 1.1rc2+ is released
    from plone.app.upgrade.v41.alphas import update_controlpanel_permissions
    update_controlpanel_permissions(context)
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
