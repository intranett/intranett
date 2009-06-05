from AccessControl import getSecurityManager
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.interfaces.plugins import ILocalRolesPlugin

class PrintInfoView(BrowserView):
    """Print debug info"""
    def getMember(self):
        memberid = self.request.get('user', None)
        membership = getToolByName(self.context, 'portal_membership')
        if memberid is None:
            return membership.getAuthenticatedMember()
        else:
            return membership.getMemberById(memberid)

    def getUser(self):
        userid = self.request.get('user', None)
        acl = getToolByName(self.context, 'acl_users')
        if userid is None:
            return getSecurityManager().getUser()
        else:
            return acl.getUserById(userid)

    def getUserId(self):
        return self.getUser().getId()

    def getGroups(self):
        try:
            return self.getUser().getGroups()
        except AttributeError:
            return ()

    def getRoles(self):
        return self.getUser().getRoles()

    def getRolesInContext(self):
        return self.getUser().getRolesInContext(self.context)

    def getMemberRolesInContext(self):
        return self.getMember().getRolesInContext(self.context)

    def getLocalroles(self):
        acl = getToolByName(self.context, 'acl_users')
        lrmanagers = acl.plugins.listPlugins(ILocalRolesPlugin)
        roles = []
        for lrid, lrmanager in lrmanagers:
            try:
                allroles = lrmanager.getAllLocalRolesInContext(self.context)
                for uid, lroles in allroles.items():
                    roles.append('%s: %s' % (uid, ', '.join(lroles)))
            except AttributeError:
                pass
        return roles


    def __call__(self):
        out = []
        out.append(DateTime().ISO())
        out.append('Use ?user=userid in URL to view results for a different user id\n')
        out.append('User %s\n' % self.getUserId())
        out.append('Groups: \n\t%s\n' % '\n\t'.join(self.getGroups()))
        out.append('Roles: \n\t%s\n' % '\n\t'.join(self.getRoles()))
        out.append('Roles in context: \n\t%s\n' % '\n\t'.join(self.getRolesInContext()))
        out.append('Member roles in context: \n\t%s\n' % '\n\t'.join(self.getMemberRolesInContext()))
        out.append('Available local roles: \n\t%s\n' % '\n\t'.join(self.getLocalroles()))
        return '\n'.join(out)
