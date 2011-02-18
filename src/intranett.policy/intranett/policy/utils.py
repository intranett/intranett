from zope.component import getUtility
from zope.component import queryUtility
from Products.CMFCore.interfaces import ISiteRoot
from intranett.policy.interfaces import IMembersFolderId


def getMembersFolderId():
    """Helper function to retrieve the members folder id."""
    return queryUtility(IMembersFolderId, default='')


def getMembersFolder():
    """Helper function to retrieve the members folder."""
    id = getMembersFolderId()
    if id:
        portal = getUtility(ISiteRoot)
        return portal.get(id)


# Make functions available to scripts
from AccessControl import ModuleSecurityInfo
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolderId')
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolder')
