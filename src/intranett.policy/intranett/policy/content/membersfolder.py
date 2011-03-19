from OFS.interfaces import IObjectWillBeRemovedEvent
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.component import getUtility
from zope.component import getSiteManager
from zope.interface import implements
from zope.lifecycleevent import IObjectMovedEvent
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import IObjectRemovedEvent

from intranett.policy.config import PROJECTNAME
from intranett.policy.interfaces import IMembersFolder
from intranett.policy.interfaces import IMembersFolderId


class MembersFolder(ATFolder):
    """This folder pretends to contain all members"""

    implements(IMembersFolder)

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


@adapter(IMembersFolder, IObjectInitializedEvent)
def registerMembersFolderId(ob, event):
    portal = getUtility(ISiteRoot)
    sm = getSiteManager(portal)
    sm.unregisterUtility(ob.id, IMembersFolderId)
    sm.registerUtility(ob.id, IMembersFolderId)

    # Reindex all member data
    mt = getToolByName(portal, 'portal_membership')
    for member in mt.listMembers():
        member.notifyModified()


@adapter(IMembersFolder, IObjectWillBeRemovedEvent)
def unregisterMembersFolderId(ob, event):
    portal = getUtility(ISiteRoot)
    sm = getSiteManager(portal)
    sm.unregisterUtility(ob.id, IMembersFolderId)


@adapter(IMembersFolder, IObjectMovedEvent)
def updateMembersFolderId(ob, event):
    if IObjectAddedEvent.providedBy(event):
        return
    if IObjectRemovedEvent.providedBy(event):
        return
    if ob != event.object: # pragma: no cover
        return
    # The members folder has been renamed
    registerMembersFolderId(ob, event)
