## Python Script "getDefaultStartEndTimes"
##bind container=container
##bind context=context
##bind namespace=
##bind subpath=traverse_subpath
##parameters=
##title=
##

from DateTime import DateTime
date = DateTime().Date()
return {'start' :   DateTime('%s 06:00' % date),
        'end'   :   DateTime('%s 23:00' % date)
        }
