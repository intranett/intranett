from AccessControl import getSecurityManager
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from intranett.policy.utils import get_personal_folder_url
from intranett.policy.utils import get_user_profile_url


class PersonalBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/personal_bar.pt')

    def update(self):
        super(PersonalBarViewlet, self).update()
        portal_state = self.portal_state
        self.anonymous = portal_state.anonymous()
        if self.anonymous:
            return

        context = self.context
        member = portal_state.member()
        userid = member.getId()

        membership = getToolByName(context, 'portal_membership')
        member_info = membership.getMemberInfo(userid)
        # member_info is None if there's no Plone user object
        if member_info:
            fullname = member_info.get('fullname', '')
        else:
            fullname = None
        if fullname:
            self.user_name = fullname
        else:
            self.user_name = userid

        sm = getSecurityManager()
        self.can_manage_users = sm.checkPermission('Manage users', self.context)
        self.profile_url = get_user_profile_url(context, userid)
        self.personal_folder_url = get_personal_folder_url(context, userid)
