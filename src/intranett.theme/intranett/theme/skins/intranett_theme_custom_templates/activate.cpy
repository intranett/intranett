## Script (Python) "activate.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Receive password reset requests
##parameters=
from Products.CMFCore.utils import getToolByName
from Products.PasswordResetTool.PasswordResetTool import InvalidRequestError, ExpiredRequestError

# Try traverse subpath first:
try:
    key = traverse_subpath[0]
except IndexError:
    key = None

# Fall back to request variable for BW compat
if not key:
    key = context.REQUEST.get('key', None)


status = state.getStatus()
pw_tool = getToolByName(context, 'portal_password_reset')
try:
    pw_tool.verifyKey(key)
except InvalidRequestError:
    status='invalid'
except ExpiredRequestError:
    status = 'expired'

return state.set(status=status, randomstring=key)
