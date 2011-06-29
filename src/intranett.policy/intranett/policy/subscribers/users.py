from zope.component import adapter

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
    # XXX
    # We need to figure out what will be happening when a principal is deleted.
    # Additionally PAS needs to be fixed to fire the IPrincipalDeletedEvent.
    # For the time being we do nothing.
    pass
