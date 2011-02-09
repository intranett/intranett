from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName

from intranett.policy.tools import Portrait

UPGRADES = []


def activate_clamav(setup):
    loadMigrationProfile(setup, 'profile-collective.ATClamAV:default')
    loadMigrationProfile(setup, 'profile-intranett.policy:default',
        steps=('propertiestool', ))
    # Move new panel up, so it's at the some position as in a new site
    cpanel = getToolByName(setup, 'portal_controlpanel')
    actions = cpanel._cloneActions()
    ids = [a.getId() for a in actions]
    clam = actions.pop(ids.index('ClamAVSettings'))
    par_id = ids.index('plone.app.registry')
    actions = actions[:par_id] + [clam] + actions[par_id:]
    cpanel._actions = tuple(actions)

UPGRADES.append((2, activate_clamav))


def disable_nonfolderish_sections(context):
    ptool = getToolByName(context, 'portal_properties')
    ptool.site_properties.disable_nonfolderish_sections = True

UPGRADES.append((3, disable_nonfolderish_sections))


def activate_collective_flag(context):
    loadMigrationProfile(context, 'profile-collective.flag:default')

UPGRADES.append((4, activate_collective_flag))


def setup_reject_anonymous(context):
    from intranett.policy import setuphandlers
    setuphandlers.setup_reject_anonymous(context)

UPGRADES.append((5, setup_reject_anonymous))


def install_MemberData_type(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('typeinfo', ))

UPGRADES.append((6, install_MemberData_type))


def update_caching_config(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('plone.app.registry', ))

UPGRADES.append((7, update_caching_config))


def migrate_image(container, id):
    image = container[id]
    # handle both str and Pdata
    data = str(image.data)
    portrait = Portrait(id=id, file=data, title='')
    portrait.manage_permission('View', ['Authenticated', 'Manager'],
        acquire=False)
    container._delObject(id)
    container._setObject(id, portrait)


def migrate_portraits(context):
    data = getToolByName(context, 'portal_memberdata')
    for k in data.portraits.keys():
        migrate_image(data.portraits, k)
    for k in data.thumbnails.keys():
        migrate_image(data.thumbnails, k)

UPGRADES.append((8, migrate_portraits))


def disable_webstats_js(context):
    ptool = getToolByName(context, 'portal_properties')
    sprops = ptool.site_properties
    sprops.webstats_js = ''

UPGRADES.append((9, disable_webstats_js))
