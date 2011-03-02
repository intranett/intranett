from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager
from zope.component import queryUtility

from intranett.policy.upgrades import upgrade_to


@upgrade_to(2)
def activate_clamav(context):
    loadMigrationProfile(context, 'profile-collective.ATClamAV:default')
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('propertiestool', ))
    # Move new panel up, so it's at the some position as in a new site
    cpanel = getToolByName(context, 'portal_controlpanel')
    actions = cpanel._cloneActions()
    ids = [a.getId() for a in actions]
    clam = actions.pop(ids.index('ClamAVSettings'))
    par_id = ids.index('plone.app.registry')
    actions = actions[:par_id] + [clam] + actions[par_id:]
    cpanel._actions = tuple(actions)


@upgrade_to(3)
def disable_nonfolderish_sections(context):
    ptool = getToolByName(context, 'portal_properties')
    ptool.site_properties.disable_nonfolderish_sections = True


@upgrade_to(4)
def activate_collective_flag(context):
    loadMigrationProfile(context, 'profile-collective.flag:default')


@upgrade_to(5)
def setup_reject_anonymous(context):
    from intranett.policy import setuphandlers
    setuphandlers.setup_reject_anonymous(context)


@upgrade_to(6)
def install_memberdata_type(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('typeinfo', ))


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
