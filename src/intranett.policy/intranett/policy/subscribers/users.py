from zope.component import adapter
from zope.component import getUtility

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.PluggableAuthService.interfaces.events import IPrincipalCreatedEvent
from Products.PluggableAuthService.interfaces.events import IPrincipalDeletedEvent

from intranett.policy.config import PERSONAL_FOLDER_ID
from intranett.policy.utils import get_personal_folder_id


@adapter(IPrincipalCreatedEvent)
def onPrincipalCreation(event):
    """
    Setup user's "personal" folder.
    """
    portal = getToolByName(event.principal, 'portal_url').getPortalObject()
    personal = portal[PERSONAL_FOLDER_ID]
    user_id = event.principal.getUserId()
    folder_id = get_personal_folder_id(user_id)
    if folder_id not in personal:
        _createObjectByType('Folder', personal, id=folder_id, title=user_id)
        folder = personal[folder_id]
        folder.processForm() # Fire events
        pu = getToolByName(personal, 'plone_utils')
        pu.changeOwnershipOf(folder, (user_id, ))
        folder.__ac_local_roles__ = None
        folder.manage_setLocalRoles(user_id, ['Owner'])


@adapter(IPrincipalDeletedEvent)
def onPrincipalDeletion(event):
    """
    Delete person folder of member.
    """
    portal = getUtility(ISiteRoot)
    personal = portal[PERSONAL_FOLDER_ID]
    user_id = event.principal
    folder_id = get_personal_folder_id(user_id)
    if folder_id in personal:
        del personal[user_id]
