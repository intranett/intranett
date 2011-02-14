from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from intranett.policy.config import PROJECTNAME


class MembersFolder(ATFolder):
    """This folder pretends to contain all members"""

    def __getitem__(self, key):
        member = getToolByName(self, 'portal_membership').getMemberById(key)
        if member is None:
            raise KeyError(key)
        return member

    def __bobo_traverse__(self, REQUEST, name):
        try:
            return self[name]
        except KeyError:
            return super(MembersFolder, self).__bobo_traverse__(REQUEST, name)


registerATCT(MembersFolder, PROJECTNAME)
