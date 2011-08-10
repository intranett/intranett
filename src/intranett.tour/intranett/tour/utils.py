from zope.component import getMultiAdapter
from zope.interface import implements

from collective.amberjack.core.interfaces import ITour


class ToursRoot(object):
    implements(ITour)

    def getTourContext(self, context, path):
        site_root = '/'.join(context.portal_url.getPortalObject().getPhysicalPath())
        if not context.portal_amberjack.sandbox:
            return context.unrestrictedTraverse(site_root + path)
        try:
            user_id = context.portal_membership.getAuthenticatedMember().id
            return context.unrestrictedTraverse(site_root + '/personal/' + user_id + path)
        except AttributeError:
            return context.unrestrictedTraverse(site_root + path)

    def getToursRoot(self, context, request, url=''):
        portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        if url:
            if url.startswith('ABS'):
                return unicode(portal_state.navigation_root_url())
        if not context.portal_amberjack.sandbox:
            return unicode(portal_state.navigation_root_url())
        user_id = context.portal_membership.getAuthenticatedMember().id
        member_folder_path = '/personal/' + user_id
        try:
            portal_state.portal().restrictedTraverse(member_folder_path.split('/')[1:])
            return unicode(portal_state.navigation_root_url() + member_folder_path)
        except AttributeError:
            return unicode(portal_state.navigation_root_url())
