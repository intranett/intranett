import patches
from zope.i18nmessageid import MessageFactory

IntranettMessageFactory = MessageFactory('intranett')

patches.apply()


def initialize(context):
    from intranett.policy.config import config
    config.register_profile()
    config.scan()

    from AccessControl import allow_module
    allow_module('intranett.policy.config')
