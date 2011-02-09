import patches

patches.apply()


def initialize(context):
    from intranett.policy.upgrades import register_upgrades
    register_upgrades()
    del register_upgrades
