BASE_PROFILE = u"Products.CMFPlone:plone"
POLICY_PROFILE = u"intranett.policy:default"
THEME_PROFILE = u"intranett.theme:default"

from pkg_resources import get_distribution
dist = get_distribution('intranett.policy')
VERSION = dist.version
del get_distribution
