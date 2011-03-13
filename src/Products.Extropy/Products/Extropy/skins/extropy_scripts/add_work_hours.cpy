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

from Products.CMFPlone.utils import safe_unicode

timetool = context.extropy_timetracker_tool

title = safe_unicode(context.Title())
addhour = timetool.addTimeTrackingHours(context, title, hours=None, start=None, end=None)

if addhour is None:
    raise Exception, "Failure adding hour"

message = u'Adding worked time record to "%s."' % title

state.setStatus('success')

context.plone_utils.addPortalMessage(message)
return state.set(context=addhour)
