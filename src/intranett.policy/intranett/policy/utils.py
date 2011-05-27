import logging

from Products.CMFCore.utils import getToolByName
from ZODB.POSException import POSKeyError
from ZODB.utils import p64
from zope.component import adapter
from zope.component import queryUtility
from zope.processlifetime import IProcessStarting

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


@adapter(IProcessStarting)
def warmupZODBCache(event):
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
            site.portal_catalog({'path': path,
                'sort_on': 'getObjPositionInParent'})
    logger.info('Warmed up ZODB cache with %d items.' % loaded)


# Make functions available to scripts
from AccessControl import ModuleSecurityInfo
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolderId')
ModuleSecurityInfo('intranett.policy.utils').declarePublic('getMembersFolder')
