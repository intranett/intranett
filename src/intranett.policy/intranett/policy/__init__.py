import patches
from zope.i18nmessageid import MessageFactory

IntranettMessageFactory = MessageFactory('intranett')

patches.apply()


def initialize(context):
    from intranett.policy.upgrades import register_upgrades
    register_upgrades()

    from intranett.policy.profile import register_profile
    register_profile()

    from intranett.policy.profile import register_import_step
    from intranett.policy.setuphandlers import various
    register_import_step(various, depends=('toolset', 'workflow'))

    from AccessControl import allow_module
    allow_module('intranett.policy.config')
