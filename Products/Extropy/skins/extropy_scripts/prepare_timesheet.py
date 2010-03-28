## Python Script "prepare_timesheet"
##bind container=container
##bind context=context
##bind namespace=
##bind subpath=traverse_subpath
##parameters=
##title=
##

#from CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
REQUEST = context.REQUEST
from DateTime import DateTime
TOOL = getattr(context,'extropy_timetracker_tool')

CURRENTUSER = getSecurityManager().getUser().getUserName()

date = DateTime().earliestTime()
starttime = DateTime('09:00')
endtime = DateTime( '16:00')

if starttime > endtime:
    mod = -1
else:
    mod = 0

startDate =  DateTime((date).Date() + ' ' + starttime.Time())
endDate   =  DateTime((date+mod).Date() + ' ' + endtime.Time())

hours = TOOL.getHours( node=None, start=startDate, end=endDate, REQUEST=None, Creator=CURRENTUSER)



results = []

a = hours[0].start.Time()
e = DateTime(a) + 1.0/24.0

print a
print e


return printed
#while DateTime(date + ' ' + a.Time())
