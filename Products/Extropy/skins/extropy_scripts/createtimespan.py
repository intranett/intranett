## Python Script "createtimespan"
##bind container=container
##bind context=context
##bind namespace=
##bind subpath=traverse_subpath
##parameters=
##title=
##


# call this script with an url like this:
# createtimespan?date:date=23/12/2005&starttime:date=09:00&endtime:date=13:00


REQUEST = context.REQUEST
from DateTime import DateTime

starttime = REQUEST.get('starttime')
endtime = REQUEST.get('endtime')
date = REQUEST.get('date').earliestTime()

if starttime > endtime:
    mod = -1
else:
    mod = 0

startDate =  DateTime((date).Date() + ' ' + starttime.Time())
endDate   =  DateTime((date+mod).Date() + ' ' + endtime.Time())

r = {'start':startDate, 'end':endDate}

return r
