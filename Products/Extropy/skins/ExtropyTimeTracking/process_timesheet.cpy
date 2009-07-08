## Controller Python Script "process_timesheet"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Add worked time
##
records = context.REQUEST.get('hours',[])
timetool = context.extropy_timetracker_tool
extropytool = context.extropy_tracking_tool
from DateTime import DateTime
request = context.REQUEST

#From the form 
date = DateTime(request.get('date',))
startstring = '%s %s' %(date, request['start'])
batchstart = DateTime( startstring )
endstring = '%s %s' %(date, request['end'])
batchend = DateTime( endstring )

added = []
for r in records:
    if r.task and r.start and r.end:
        start = DateTime('%s %s' % (date,r.start ))
        end = DateTime('%s %s' % (date,r.end ))
        if start > end:
            mod = +1
        else:
            mod = 0
        worktask = extropytool(UID=r.task)
        if worktask:
            o = worktask[0].getObject()
            addhour = timetool.addTimeTrackingHours(o, o.Title(), hours=None, start=start, end=end+mod)
            if addhour is None:
                raise Exception, "Failure adding hours"
            added.append(o.Title())
if added:
    message = "added workhours to " + ", ".join(added)
    state.setStatus('success')
else:
    if not added and (context.REQUEST.get('start') or context.REQUEST.get('end')):
        message = "changed timespan"
        state.setStatus('settimes')
    else:
        message = "no hours added"
        state.setStatus('failure')

return state.set(context=context, portal_status_message=message)
