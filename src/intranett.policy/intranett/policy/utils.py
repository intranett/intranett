import logging
from urllib import quote

from Acquisition import aq_get
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


def get_fullname(context, userid):
    membership = getToolByName(context, 'portal_membership')
    member_info = membership.getMemberInfo(userid)
    # member_info is None if there's no Plone user object
    if member_info:
        fullname = member_info.get('fullname', '')
    else: # pragma: no cover
        fullname = None
    if fullname:
        return fullname
    return userid


def getMembersFolderId():
    """Helper function to retrieve the members folder id."""
    return queryUtility(IMembersFolderId, default='')


def get_users_folder_url(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    return portal.absolute_url() + '/' + quote(getMembersFolderId())


def get_user_profile_url(context, member_id):
    return get_users_folder_url(context) + '/' + quote(member_id)


def get_current_user_profile_url(context):
    mtool = getToolByName(context, "portal_membership")
    member = mtool.getAuthenticatedMember()
    userid = member.getId()
    return get_users_folder_url(context) + '/' + quote(userid)


def getMembersFolder(context):
    """Helper function to retrieve the members folder."""
    id = getMembersFolderId()
    if id:
        portal = getToolByName(context, 'portal_url').getPortalObject()
        return portal.get(id)


def quote_userid(user_id):
    if isinstance(user_id, unicode):
        user_id = user_id.encode('utf-8')
    return cleanId(user_id)


def get_personal_folder(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    return portal.get(PERSONAL_FOLDER_ID, None)


def get_personal_folder_url(context, userid):
    personal = get_personal_folder(context)
    if personal is None: # pragma: no cover
        return
    folder_id = quote_userid(userid)
    folder = personal.get(folder_id, None)
    if folder is None:
        return
    return folder.absolute_url()


def create_personal_folder(context, user_id):
    personal = get_personal_folder(context)
    if personal is None:
        return
    folder_id = quote_userid(user_id)
    if folder_id not in personal:
        # don't let the request interfere in the processForm call
        request = aq_get(personal, 'REQUEST', None)
        if request is not None:
            fullname = get_fullname(context, user_id)
            # if we create a new user ttw - the memberdata isn't yet set when
            # we call this, take it directly from the request
            if fullname == user_id:
                fullname = request.form.get('form.fullname', fullname)
            request.form['title'] = fullname
        _createObjectByType('Folder', personal, id=folder_id, title=fullname)
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
ModuleSecurityInfo('intranett.policy.utils').declarePublic(
    'get_current_user_profile_url')
