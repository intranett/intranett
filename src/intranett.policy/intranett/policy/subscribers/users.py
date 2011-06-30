from zope.component import adapter
from zope.component import getUtility

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.PlonePAS.utils import cleanId
from Products.PluggableAuthService.interfaces.events import IPrincipalCreatedEvent
from Products.PluggableAuthService.interfaces.events import IPrincipalDeletedEvent

from intranett.policy.config import PERSONAL_FOLDER_ID


@adapter(IPrincipalCreatedEvent)
def onPrincipalCreation(event):
    """
    Setup user's "personal" folder.
    """
    portal = getToolByName(event.principal, 'portal_url').getPortalObject()
    personal = portal[PERSONAL_FOLDER_ID]
    user_id = event.principal.getUserId()
    user_id_str = user_id
    if isinstance(user_id_str, unicode):
        user_id_str = user_id_str.encode('utf-8')
    user_id_str = cleanId(user_id_str)
    if user_id_str not in personal:
        _createObjectByType('Folder', personal, id=user_id_str, title=user_id)
        folder = personal[user_id_str]
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
    if isinstance(user_id, unicode):
        user_id = user_id.encode('utf-8')
    user_id = cleanId(user_id)
    if user_id in personal:
        del personal[user_id]
