## Controller Python Script "tasks_add1on1"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Create 1-on-1 task (copying deliverable metadata)
##

from Products.CMFCore.utils import getToolByName

plone_tool = getToolByName(context, 'plone_utils', None)
wf_tool = getToolByName(context, 'portal_workflow', None)

new_id = context.generateUniqueId(type_name='ExtropyTask')
context.invokeFactory('ExtropyTask', new_id, title=context.Title(),
                      description=context.Description(), 
                      text=context.getRawText(),
                      responsiblePerson=context.getResponsiblePerson())
new_task = getattr(context, new_id)
if new_task.getResponsiblePerson():
    wf_tool.doActionFor(new_task, 'assign')

message = 'Added 1-on-1 task'

state.setStatus('success')

return state.set(context=context, portal_status_message=message)
