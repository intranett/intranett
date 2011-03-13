from DateTime  import DateTime

timetool = context.extropy_timetracker_tool
year = DateTime().year()
quarters = {
                         1:('%s/01/01'%year,'%s/03/31'%year),
                         2:('%s/04/01'%year,'%s/06/30'%year),
                         3:('%s/07/01'%year,'%s/09/30'%year),
                         4:('%s/10/01'%year,'%s/12/31'%year)}
quarter = DateTime().month() / 3 + bool(DateTime().month() % 3)
qstart = DateTime(quarters[quarter][0])
qend = DateTime(quarters[quarter][1])

context.REQUEST.set('startdate',str(qstart))
context.REQUEST.set('endate',str(qend))

text="""Hi,

This is an automated email. We will send one like it every month with a summary of the support incidents handled so far in the current quarter.

If there are any questions regarding this report or anything else regarding your support contract please reply to this email. 


"""
statustext = ""

mailhost = context.MailHost
mFrom = 'support@jarn.com'

for package in context.getFolderContents(contentFilter={'portal_type':"ExtropyPhase", 'review_state':'active'}):
    if package.getId=="support-administration":
        continue
    pobj = package.getObject()
    email = pobj.getClientNotifyEmail()
    if email == '':
        continue
    title="%s\n"%package.Title
    mSubj = 'Jarn Support report for quarter %s as of %s'%(quarter,DateTime().Date())
    statustext +="Sent email to %s of %s\n"%(email, package.getId)
    emailhours= pobj.restrictedTraverse( '@@email_hours_report')()
    mailhost.send(text+ title+emailhours, email, mFrom, mSubj)

mailhost.send(statustext, 'martior@jarn.com', mFrom, 'Status of support-report for quarter %s as of %s'%(quarter,DateTime().Date()))
print "ok"
