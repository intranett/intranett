## Controller Python Script "process_timesheet_fast"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Add worked time
##

from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode

records = context.REQUEST.get('hours',[])
timetool = context.extropy_timetracker_tool
extropytool = context.extropy_tracking_tool
request = context.REQUEST

#From the form 
date = DateTime(request.get('date',))

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
            title = r.title and r.title or o.Title()
            addhour = timetool.addTimeTrackingHours(o, title, hours=None, start=start, end=end+mod)
            if addhour is None:
                raise Exception, "Failure adding hours"
            addhour.setSummary(r.summary, mimetype="text/x-rst")
            added.append(safe_unicode(title))
            request.set('last_task', r.task)
if added:
    message = u"Added workhours to " + u", ".join(added)
    state.setStatus('success')
else:
    if not added:
        message = u"Changed timespan"
        state.setStatus('settimes')
    else:
        message = u"No hours added"
        state.setStatus('failure')

context.plone_utils.addPortalMessage(message)
return state.set(context=context)
