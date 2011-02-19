from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from intranett.policy.interfaces import IMembersFolderId


def getMembersFolderId():
    """Helper function to retrieve the members folder id."""
    return queryUtility(IMembersFolderId, default='')


def getMembersFolder(context):
    """Helper function to retrieve the members folder."""
    id = getMembersFolderId()
    if id:
        portal = getToolByName(context, 'portal_url').getPortalObject()
        return portal.get(id)


# Make functions available to scripts
from AccessControl import ModuleSecurityInfo
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolderId')
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolder')
