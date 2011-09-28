## Controller Python Script "invite"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=invite_to_address, message='', enforce_address=False, came_from_portlet=False
##title=Send an URL to a friend
##

from Products.CMFCore.utils import getToolByName
from Products.PloneInvite import PloneInviteMessageFactory as _
from intranett.policy.browser.invitation import sendInvitationMail

portal_invitations = getToolByName(context,'portal_invitations')
putils = getToolByName(context,'plone_utils')

# Get invite and send it
member = context.portal_membership.getAuthenticatedMember()
invitecode = portal_invitations.getInviteCode(enforce_address)
variables = {'invite_to_address' : invite_to_address,
             'message' : message,
             'enforce_address' : enforce_address,
             'invitecode' : invitecode,
            }
site = getToolByName(context, 'portal_url').getPortalObject()
sendInvitationMail(site, member, variables)

# Mark this invite as sent.
portal_invitations.invites[invitecode].sendTo(invite_to_address)

portalmessage = _(u"Sent invitation to %s.") % invite_to_address

putils.addPortalMessage(portalmessage)

if came_from_portlet:
    state.set(status='from_portlet')

return state
