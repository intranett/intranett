## Script (Python) "activate_action.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Reset a user's password
##parameters=randomstring, userid=None, password=None, password2=None
from Products.CMFCore.utils import getToolByName
from Products.PasswordResetTool.PasswordResetTool import InvalidRequestError, ExpiredRequestError
from intranett.policy.browser.activation import loginUser

status = "success"
pw_tool = getToolByName(context, 'portal_password_reset')
try:
    pw_tool.resetPassword(userid, randomstring, password)
except ExpiredRequestError:
    status = "expired"
except InvalidRequestError:
    status = "invalid"
except RuntimeError:
    status = "invalid"
else:
    loginUser(context, userid, password)

return state.set(status=status)
