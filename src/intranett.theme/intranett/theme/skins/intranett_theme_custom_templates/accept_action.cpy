## Controller Python Script "accept_action"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=password='password', password_confirm='password_confirm', came_from_prefs=None
##title=Register a User
##

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from intranett.policy.browser.activation import loginUser

REQUEST = context.REQUEST

portal = context.portal_url.getPortalObject()
portal_registration = context.portal_registration

username = REQUEST['username']
password = REQUEST['password']

try:
    portal_registration.addMember(username, password, properties=REQUEST, REQUEST=REQUEST)
except AttributeError:
    state.setError('username', _(u'The login name you selected is already in use or is not valid. Please choose another.'))
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'), 'error')
    return state.set(status='failure')

inv_tool = getToolByName(context, 'portal_invitations')
key = context.REQUEST['invite_code']
invite = inv_tool.invites[key]
invite.useInvite(key, username)

state.set(came_from=REQUEST.get('came_from','login_success'))

from Products.CMFPlone.utils import transaction_note
transaction_note('%s registered' % username)

loginUser(context, username, password)

return state
