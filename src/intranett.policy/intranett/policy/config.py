PROJECTNAME = 'intranett.policy'
ADD_PERMISSIONS = {'MembersFolder': '%s: Add MembersFolder' % PROJECTNAME}
MEMBERS_FOLDER_ID = 'people'
MEMBERS_FOLDER_TITLE = 'People'

BASE_PROFILE = u"Products.CMFPlone:plone"
POLICY_PROFILE = u"intranett.policy:default"
THEME_PROFILE = u"intranett.theme:default"

from pkg_resources import get_distribution
dist = get_distribution(PROJECTNAME)
VERSION = dist.version
del get_distribution
