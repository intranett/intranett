from AccessControl import getSecurityManager
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from intranett.policy.utils import get_fullname
from intranett.policy.utils import get_personal_folder_url
from intranett.policy.utils import get_user_profile_url


class PersonalBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/personal_bar.pt')

    def update(self):
        super(PersonalBarViewlet, self).update()
        context = self.context
        mtool = getToolByName(context, "portal_membership")
        self.anonymous = bool(mtool.isAnonymousUser())
        if self.anonymous:
            return

        sm = getSecurityManager()
        member = mtool.getAuthenticatedMember()
        userid = member.getId()
        self.user_name = get_fullname(context, userid)
        self.can_manage_users = sm.checkPermission('Manage users', self.context)
        self.profile_url = get_user_profile_url(context, userid)
        self.personal_folder_url = get_personal_folder_url(context, userid)
