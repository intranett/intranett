import logging

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.PlonePAS.utils import cleanId
from ZODB.POSException import POSKeyError
from ZODB.utils import p64
from zope.component import adapter
from zope.component import queryUtility
from zope.processlifetime import IProcessStarting

from intranett.policy.config import PERSONAL_FOLDER_ID
from intranett.policy.interfaces import IMembersFolderId

logger = logging.getLogger("intranett")


def getMembersFolderId():
    """Helper function to retrieve the members folder id."""
    return queryUtility(IMembersFolderId, default='')


def getMembersFolder(context):
    """Helper function to retrieve the members folder."""
    id = getMembersFolderId()
    if id:
        portal = getToolByName(context, 'portal_url').getPortalObject()
        return portal.get(id)


def get_personal_folder_id(user_id):
    if isinstance(user_id, unicode):
        user_id = user_id.encode('utf-8')
    return cleanId(user_id)


def create_personal_folder(context, user_id):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    personal = portal.get(PERSONAL_FOLDER_ID, None)
    if personal is None:
        return
    folder_id = get_personal_folder_id(user_id)
    if folder_id not in personal:
        _createObjectByType('Folder', personal, id=folder_id, title=user_id)
        folder = personal[folder_id]
        folder.processForm() # Fire events
        pu = getToolByName(personal, 'plone_utils')
        pu.changeOwnershipOf(folder, (user_id, ))
        folder.__ac_local_roles__ = None
        folder.manage_setLocalRoles(user_id, ['Owner'])
        folder.setCreators([user_id])
        folder.reindexObject()


@adapter(IProcessStarting)
def warmupZODBCache(event): # pragma: no cover
    logger.info('Warming up ZODB cache.')
    import Zope2
    cache_size = Zope2.DB.getCacheSize()
    with Zope2.DB.transaction() as conn:
        loaded = 0
        for i in range(1, cache_size * 2):
            try:
                obj = conn.get(p64(i))
            except POSKeyError:
                continue
            obj._p_activate()
            loaded += 1
            if loaded >= cache_size:
                break
        sites = conn.root()['Application'].objectValues('Plone Site')
        if sites:
            site = sites[0]
            path = {'query': '/'.join(site.getPhysicalPath()), 'depth': 1}
            site.portal_catalog({'path': path, 'sort_on': 'path'})
    logger.info('Warmed up ZODB cache with %d items.' % loaded)


# Make functions available to scripts
from AccessControl import ModuleSecurityInfo
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolderId')
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolder')
