from intranett.policy.plutonian import Configurator
config = Configurator('intranett.policy')

BASE_PROFILE = u"Products.CMFPlone:plone"
POLICY_PROFILE = config.policy_profile
THEME_PROFILE = u"intranett.theme:default"
