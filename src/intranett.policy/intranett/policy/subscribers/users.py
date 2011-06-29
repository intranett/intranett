from zope.component import adapter
from zope.component import getUtility

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.events import IPrincipalCreatedEvent
from Products.PluggableAuthService.interfaces.events import IPrincipalDeletedEvent


@adapter(IPrincipalCreatedEvent)
def onPrincipalCreation(event):
    """
    Setup user's "personal" folder.
    """
    portal = getToolByName(event.principal, 'portal_url').getPortalObject()
    personal = portal['personal']
    user_id = event.principal.getUserId()
    if user_id not in personal:
        personal.invokeFactory('Folder', user_id, title=user_id)
        folder = personal[user_id]
        pu = getToolByName(personal, 'plone_utils')
        pu.changeOwnershipOf(folder, (user_id, ))


@adapter(IPrincipalDeletedEvent)
def onPrincipalDeletion(event):
    """
    Delete person folder of member.
    """
    portal = getUtility(ISiteRoot)
    personal = portal['personal']
    user_id = event.principal
    if user_id in personal:
        del personal[user_id]
