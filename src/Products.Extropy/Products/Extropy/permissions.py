from Products.CMFCore.permissions import *

VIEW_PERMISSION             = View
ADD_CONTENT_PERMISSION     = AddPortalContent
MODIFY_CONTENT_PERMISSION = ModifyPortalContent

# some permissions we need
ADD_COMMENTS_TO_TASKS_PERMISSION = None

MANAGE_PLAN_ITEMS = 'Extropy: Manage plan items'
MANAGE_FINANCES = "Extropy: Finances"
PARTICIPATE = "Extropy: Participate"
OBSERVE = "Extropy: Observe"
MANAGE_PROJECTS = "Extropy: Manage Projects"


setDefaultRoles(MANAGE_FINANCES, ())
setDefaultRoles(PARTICIPATE, ('Manager',))
setDefaultRoles(OBSERVE, ('Manager',))
setDefaultRoles(MANAGE_PROJECTS, ('Manager',))
