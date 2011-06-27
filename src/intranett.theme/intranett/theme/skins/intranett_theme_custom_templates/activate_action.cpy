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
    context.REQUEST.set('__ac_name', userid)
    context.REQUEST.set('__ac_password', password)

return state.set(status=status)
