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

for entry in context.REQUEST.featureadd:
    if entry:
        new_id = plone_tool.normalizeString(entry)
        context.invokeFactory('ExtropyFeature',new_id, title=entry)

message = 'Added deliverables to "%s."' % context.Title()

state.setStatus('success')

return state.set(context=context, portal_status_message=message)
