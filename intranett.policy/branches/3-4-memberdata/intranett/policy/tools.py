from OFS.Image import Image
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import _checkPermission
from Products.PlonePAS.tools.membership import MembershipTool as BaseMembershipTool
from Products.PlonePAS.tools.memberdata import MemberDataTool as BaseMemberDataTool
from Products.PlonePAS.tools.membership import default_portrait
from Products.PlonePAS.utils import scale_image

PORTRAIT_SIZE = (300, 300,)
PORTRAIT_THUMBNAIL_SIZE = (100, 100,)

class MemberDataTool(BaseMemberDataTool):

    def __init__(self):
        super(MemberDataTool, self).__init__()
        self.thumbnails = BTreeFolder2(id='thumbnails')

    def _getPortrait(self, member_id, thumbnail=False):
        "return member_id's portrait if you can "
        if thumbnail:
            return self.thumbnails.get(member_id, None)
        return super(MemberDataTool, self)._getPortrait(member_id)

    def _setPortrait(self, portrait, member_id, thumbnail=False):
        " store portrait which must be a raw image in _portrais "
        if thumbnail:
            if member_id in self.thumbnails:
                self.thumbnails._delObject(member_id)
            self.thumbnails._setObject(id=member_id, object=portrait)
        else:
            super(MemberDataTool, self)._setPortrait(portrait, member_id)

    def _deletePortrait(self, member_id):
        " remove member_id's portrait "
        super(MemberDataTool, self)._deletePortrait(member_id)
        if member_id in self.thumbnails:
            self.thumbnails._delObject(member_id)


class MembershipTool(BaseMembershipTool):

    def changeMemberPortrait(self, portrait, id=None):
        """update the portait of a member.

        Modified from CMFPlone version to URL-quote the member id.
        """
        safe_id = self._getSafeMemberId(id)
        if not safe_id:
            safe_id = self.getAuthenticatedMember().getId()

        membertool = getToolByName(self, 'portal_memberdata')
        if portrait and portrait.filename:
            #import pdb; pdb.set_trace( )
            scaled, mimetype = scale_image(portrait,
                                           max_size=PORTRAIT_SIZE)
            image = Image(id=safe_id, file=scaled, title='')
            membertool._setPortrait(image, safe_id)
            # Now for thumbnails
            portrait.seek(0)
            scaled, mimetype = scale_image(portrait,
                                           max_size=PORTRAIT_THUMBNAIL_SIZE)
            image = Image(id=safe_id, file=scaled, title='')
            membertool._setPortrait(image, safe_id, thumbnail=True)

    def getPersonalPortrait(self, id=None, verifyPermission=0, thumbnail=True):
        """Return a members personal portait.

        Modified to make it possible to return the thumbnail portrait.
        """
        safe_id = self._getSafeMemberId(id)
        membertool   = getToolByName(self, 'portal_memberdata')

        if not safe_id:
            safe_id = self.getAuthenticatedMember().getId()

        portrait = membertool._getPortrait(safe_id, thumbnail=thumbnail)
        if isinstance(portrait, str):
            portrait = None
        if portrait is not None:
            if verifyPermission and not _checkPermission('View', portrait):
                # Don't return the portrait if the user can't get to it
                portrait = None
        if portrait is None:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            portrait = getattr(portal, default_portrait, None)

        return portrait
