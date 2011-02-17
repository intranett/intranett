from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot


def getMembersFolder():
    """Helper function to retrieve the members folder."""
    folders = getUtility(ISiteRoot).objectValues(['MembersFolder'])
    if folders:
        return folders[0]


def getMembersFolderId():
    """Helper function to retrieve the members folder id."""
    folder = getMembersFolder()
    if folder is not None:
        return folder.getId()
    return ''


from AccessControl import ModuleSecurityInfo
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolder')
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolderId')
