from collective.amberjack.core.interfaces import ITour
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.interface import implements

from intranett.policy.config import PERSONAL_FOLDER_ID


class ToursRoot(object):
    implements(ITour)

    def getTourContext(self, context, path):
        amberjack = getToolByName(context, 'portal_amberjack')
        mtool = getToolByName(context, 'portal_membership')
        portal_url = getToolByName(context, 'portal_url')
        site = portal_url.getPortalObject()
        if not amberjack.sandbox:
            return site.unrestrictedTraverse(path)
        try:
            user_id = mtool.getAuthenticatedMember().id
            return site.unrestrictedTraverse(
                '%s/' % PERSONAL_FOLDER_ID + user_id + path)
        except AttributeError:
            return site.unrestrictedTraverse(path)

    def getToursRoot(self, context, request, url=''):
        amberjack = getToolByName(context, 'portal_amberjack')
        mtool = getToolByName(context, 'portal_membership')
        portal_state = getMultiAdapter(
            (context, request), name=u'plone_portal_state')
        navroot = unicode(portal_state.navigation_root_url())
        if url and url.startswith('ABS'):
            return navroot
        if not amberjack.sandbox:
            return navroot
        user_id = mtool.getAuthenticatedMember().id
        member_folder_path = '/%s/' % PERSONAL_FOLDER_ID + user_id
        try:
            portal_state.portal().restrictedTraverse(member_folder_path.split('/')[1:])
            return navroot + unicode(member_folder_path)
        except AttributeError:
            return navroot
