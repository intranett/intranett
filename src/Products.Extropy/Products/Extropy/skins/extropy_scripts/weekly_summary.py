## Script (Python) "weekly_summary"
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

def heading(txt):
  txt = '-' * 5 + txt + '-' * 72
  return txt[:72]

def fmtName(item):
    name = str(item)
    info = mtool.getMemberInfo(name)
    fullname = info and info.get('fullname')
    fullname = fullname.split(' ')[0]
    if fullname == 'Thor': fullname += ' Arne'
    return str(unicode(fullname and fullname or name, 'utf-8'))

def fmtNumber(number):
  return '%.1f' % number

if start is None:
  start = DateTime().earliestTime()-7

if end is None:
  if start is not None:
    end = DateTime(start)+7
  else:
    end = DateTime().earliestTime()

view = context.restrictedTraverse('@@hourreport_view')
info = {}

# total hours
results = view.getReportData(start=start,end=end)
for node in results:
  hours = info.setdefault(fmtName(node.getKey()), {})
  hours['total'] = node.getValue()
totals = results.getValue()

# billable hours
results = view.getReportData(start=start,end=end, getBudgetCategory='Billable')
for node in results:
  hours = info.setdefault(fmtName(node.getKey()), {})
  hours['billable'] = node.getValue()
billables = results.getValue()

info = info.items()
info.sort(cmp=lambda a,b: cmp(a[0], b[0]))

print heading('Version for IRC')
print 'Weekly hour report for week %s (%s — %s):' % (start.week(), start, end - 1)
for person, hours in info:
  billable = fmtNumber(hours.get('billable', 0))
  total = fmtNumber(hours.get('total', 0))
  print '  %s did %s hours (%s billable)' % (person, total, billable)

# print the totals & weekly status
print 'Totals: %s hours (%s billable)' % (totals, billables)
diff = billables - 200
if diff >= 0:
    status = ':-) (%s over)' % diff
else:
    status = ':-( (%s under)' % -diff
print 'Status: %s' % status

# print another report for the summary
print '\n' + heading('Version for weekly summary')

print 'Weekly hour report for week %s (%s — %s):\n' % (start.week(), start, end - 1)
for person, hours in info:
  billable = fmtNumber(hours.get('billable', 0))
  total = fmtNumber(hours.get('total', 0))
  print '%s\n  %s hours (%s billable)' % (person, total, billable)

# print the totals & weekly status
print 'Total:\n  %s hours (%s billable)' % (totals, billables)
print 'Status:\n  %s' % status

return printed
