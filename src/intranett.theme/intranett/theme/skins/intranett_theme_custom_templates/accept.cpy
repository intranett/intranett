## Script (Python) "accept.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Accept an invitation
##parameters=
from Products.CMFCore.utils import getToolByName

# Try traverse subpath first:
try:
    key = traverse_subpath[0]
except IndexError:
    key = None

# Fall back to request variable for BW compat
if not key:
    key = context.REQUEST.get('key', None)


status = state.getStatus()
inv_tool = getToolByName(context, 'portal_invitations')

invite = inv_tool.invites.get(key, None)
if invite is None:
    status = 'invalid'
elif invite.used:
    status = 'expired'

context.REQUEST.form['invite_code'] = key
return state.set(status=status, randomstring=key)
