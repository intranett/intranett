from zope.component import getUtility

from plone.app.upgrade.utils import loadMigrationProfile
from plutonian.gs import upgrade_to


@upgrade_to(46)
def remove_unused_workflows(context):
    from intranett.policy.setuphandlers import remove_unused_workflows
    remove_unused_workflows(context)


@upgrade_to(47)
def install_xmpp(context):
    loadMigrationProfile(context, 'profile-jarn.xmpp.core:default')
    loadMigrationProfile(context, 'profile-intranett.policy:default',
        steps=('cssregistry', 'jsregistry', 'kssregistry', 'plone.app.registry', ))
    loadMigrationProfile(context, 'profile-intranett.theme:default',
        steps=('viewlets', ))

    # Setup existing users
    from jarn.xmpp.twisted.testing import wait_for_client_state
    from jarn.xmpp.core.interfaces import IAdminClient
    from jarn.xmpp.core.subscribers.startup import setupAdminClient
    from jarn.xmpp.core.utils.setup import setupXMPPEnvironment
    setupAdminClient(None, None)

    client = getUtility(IAdminClient)
    wait_for_client_state(client, 'authenticated')
    setupXMPPEnvironment(context)
