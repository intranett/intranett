from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName

from intranett.policy.tools import Portrait


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


def disable_nonfolderish_sections(context):
    ptool = getToolByName(context, 'portal_properties')
    ptool.site_properties.disable_nonfolderish_sections = True


def activate_collective_flag(context):
    loadMigrationProfile(context, 'profile-collective.flag:default')


def install_MemberData_type(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default', 
        steps=('typeinfo',))


def update_caching_config(context):
    loadMigrationProfile(context, 'profile-intranett.policy:default', 
        steps=('plone.app.registry',))


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
