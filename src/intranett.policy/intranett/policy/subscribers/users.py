from zope.component import adapter

from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.events import IPrincipalCreatedEvent


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
