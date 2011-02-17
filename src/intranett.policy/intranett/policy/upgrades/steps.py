from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName

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
def install_people_folder(context):
    # Remove the employee-listing action
    atool = getToolByName(context, 'portal_actions')
    if 'employee-listing' in atool.portal_tabs:
        atool.portal_tabs._delObject('employee-listing')
    # Add the MembersFolder portal type
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('typeinfo', 'factorytool'))
    # Add the people folder
    from intranett.policy.utils import getMembersFolder
    from intranett.policy.setuphandlers import setup_people_folder
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if getMembersFolder() is None:
        setup_people_folder(portal)
