## Controller Python Script "batch_create_deliverabes"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=create
##

from Products.CMFCore.utils import getToolByName

plone_tool = getToolByName(context, 'plone_utils', None)
wf_tool = getToolByName(context, 'portal_workflow', None)

for entry in context.REQUEST.taskadd:
    if entry.title:
        new_id = context.generateUniqueId(type_name='ExtropyTask')
        context.invokeFactory('ExtropyTask', new_id, title=entry.title,
                              responsiblePerson=entry.responsible)
        new_task = getattr(context, new_id)
        if new_task.getResponsiblePerson():
            wf_tool.doActionFor(new_task, 'assign')

message = 'Added tasks to "%s."' % context.Title()

state.setStatus('success')

return state.set(context=context, portal_status_message=message)
