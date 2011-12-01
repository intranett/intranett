from plone.app.upgrade.utils import loadMigrationProfile
from plutonian.gs import upgrade_to


@upgrade_to(46)
def remove_unused_workflows(context):
    from intranett.policy.setuphandlers import remove_unused_workflows
    remove_unused_workflows(context)


@upgrade_to(47)
def install_xmpp(context):
    from intranett.policy.setuphandlers import setup_xmpp
    loadMigrationProfile(context, 'profile-jarn.xmpp.core:default')
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('cssregistry', 'jsregistry', 'kssregistry', 'plone.app.registry', ))
    loadMigrationProfile(context, 'profile-intranett.theme:default',
        steps=('viewlets', ))
    setup_xmpp(context)
