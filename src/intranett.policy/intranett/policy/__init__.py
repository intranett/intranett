import patches
from zope.i18nmessageid import MessageFactory

IntranettMessageFactory = MessageFactory('intranett')

patches.apply()


def initialize(context):
    from intranett.policy.upgrades import register_upgrades
    register_upgrades()

    from intranett.policy.profile import register_profile
    register_profile()

    from intranett.policy.profile import register_import_steps
    from intranett.policy import setuphandlers
    setuphandlers # load handlers
    register_import_steps()

    from AccessControl import allow_module
    allow_module('intranett.policy.config')
