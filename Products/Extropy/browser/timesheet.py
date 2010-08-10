from zope.publisher.browser import BrowserView

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode


class TimeSheet(BrowserView):


    def __call__(self):
        if 'form.submitted' in self.request.form:
            self.process()
        return super(TimeSheet, self).__call__()

    def process(self):
        context = self.context
        request = self.request

        records = request.get('hours',[])
        timetool = getToolByName(context, 'extropy_timetracker_tool')
        extropytool = getToolByName(context, 'extropy_tracking_tool')

        # From the form 
        date = DateTime(request.get('date'))

        added = []
        for r in records:
            if r.task and r.start and r.end:
                start = DateTime('%s %s' % (date ,r.start))
                end = DateTime('%s %s' % (date, r.end))
                if start > end:
                    mod = 1
                else:
                    mod = 0
                worktask = extropytool(UID=r.task)
                if worktask:
                    o = worktask[0].getObject()
                    title = r.title and r.title or o.Title()
                    addhour = timetool.addTimeTrackingHours(
                        o, title, hours=None, start=start, end=end + mod)
                    if addhour is None:
                        raise Exception("Failure adding hours")
                    addhour.setSummary(r.summary, mimetype="text/x-rst")
                    added.append(safe_unicode(title))
                    request.set('last_task', r.task)
        if added:
            message = u"Added workhours to " + u", ".join(added)
        else:
            if not added:
                message = u"Changed timespan"
            else:
                message = u"No hours added"

        context.plone_utils.addPortalMessage(message)
