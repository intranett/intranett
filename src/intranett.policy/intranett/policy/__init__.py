import patches

patches.apply()


def initialize(context):
    from intranett.policy.upgrades import register_upgrades
    register_upgrades()

    from AccessControl import allow_module
    allow_module('intranett.policy.config')
