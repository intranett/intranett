## Controller Python Script "add_work_hours"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Add worked time
##

timetool = context.extropy_timetracker_tool
addhour = timetool.addTimeTrackingHours(context, context.Title(), hours=None, start=None, end=None)

if addhour is None:
    raise Exception, "Failure adding hour"

message = 'Adding worked time record to "%s."' % context.Title()

state.setStatus('success')

return state.set(context=addhour, portal_status_message=message)
