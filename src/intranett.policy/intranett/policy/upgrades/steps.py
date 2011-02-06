from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName


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
