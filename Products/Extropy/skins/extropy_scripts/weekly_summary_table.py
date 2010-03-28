## Script (Python) "weekly_summary_table"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=start=None, end=None
##title=
##
from Products.CMFCore.utils import getToolByName
mtool = getToolByName(context, 'portal_membership')
context.REQUEST.response.setHeader('Content-Type', 'text/plain; charset="utf-8"')

def fmtName(item):
    name = str(item)
    info = mtool.getMemberInfo(name)
    fullname = info and info.get('fullname')
    return '%-16s' % unicode(fullname and fullname or name, 'utf-8')

def fmtNumber(number):
  return '%4.1f' % number

if start is None:
  start = DateTime().earliestTime()-7

if end is None:
  end = DateTime().earliestTime()

view = context.restrictedTraverse('@@hourreport_view')
group_by = 'Creator:start/Day'
results = view.getReportData(start=start,end=end,group_by=group_by)

print '+------------------+------+------+------+------+------+------+------+------+'
print '|                  | Mon  | Tue  | Wed  | Thu  | Fri  | Sat  | Sun  | Tot  |'
print '+==================+======+======+======+======+======+======+======+======+'

for node in results:
  zero = fmtNumber(0)
  info = {
    'Name': fmtName(node.getKey()),
    'Total': fmtNumber(node.getValue()),
    'Monday': zero,
    'Tuesday': zero,
    'Wednesday': zero,
    'Thursday': zero,
    'Friday': zero,
    'Saturday': zero,
    'Sunday': zero,
  }
  for day in node:
    info.update({day.getKey(): fmtNumber(day.getValue())})
  print '| %(Name)s | %(Monday)s | %(Tuesday)s | %(Wednesday)s | %(Thursday)s | %(Friday)s | %(Saturday)s | %(Sunday)s | %(Total)s |' % info
  print '+------------------+------+------+------+------+------+------+------+------+'

return printed
