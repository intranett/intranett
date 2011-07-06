from Products.CMFCore.interfaces import ISiteRoot
from Products.PluggableAuthService.interfaces.events import (
    IPrincipalCreatedEvent, IPrincipalDeletedEvent)
from zope.component import adapter
from zope.component import getUtility

from intranett.policy.config import PERSONAL_FOLDER_ID
from intranett.policy.utils import create_personal_folder
from intranett.policy.utils import quote_userid


@adapter(IPrincipalCreatedEvent)
def onPrincipalCreation(event):
    """
    Setup user's "personal" folder.
    """
    create_personal_folder(event.principal, event.principal.getUserId())


@adapter(IPrincipalDeletedEvent)
def onPrincipalDeletion(event):
    """
    Delete person folder of member.
    """
    portal = getUtility(ISiteRoot)
    personal = portal.get(PERSONAL_FOLDER_ID, None)
    if personal is None: # pragma: no cover
        return
    user_id = event.principal
    folder_id = quote_userid(user_id)
    if folder_id in personal:
        del personal[user_id]
