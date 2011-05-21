from Products.PythonScripts.standard import html_quote
request = container.REQUEST
response =  request.response

#request.RESPONSE.setHeader('Content-Type','application/csv')

print ';'.join([str(i) for i in["Date", "Hours", "Title", "Person", "Project", "Path"]])
tttool = context.extropy_timetracker_tool
hours = tttool.getHours(node=context)

for h in hours:
    print ';'.join([str(i) for i in[h.start.ISO().split('T')[0], float(h.workedHours), h.Title, h.Creator, h.getObject().aq_parent.aq_parent.Title() , h.getPath()]])

return printed
