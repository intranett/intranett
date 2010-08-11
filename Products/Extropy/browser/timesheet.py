# -*- coding: utf-8 -*-

from zope.publisher.browser import BrowserView

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from Products.Extropy.odict import OrderedDict


class TimeSheet(BrowserView):

    def __call__(self):
        if 'form.submitted' in self.request.form:
            return self.request.response.redirect(self.process())
        return super(TimeSheet, self).__call__()

    def startend(self):
        datestring = self.request.form.get('date', DateTime().Date())
        start = DateTime('%s %s' % (datestring, '00:00'))
        end = DateTime('%s %s' % (datestring, '23:59'))
        return {'start': start, 'end': end}

    def timetool(self):
        return getToolByName(self.context, 'extropy_timetracker_tool')

    def extropytool(self):
        return getToolByName(self.context, 'extropy_tracking_tool')

    def hours(self, start, end, username):
        timetool = self.timetool()
        result = timetool.getHours(
            self.context, start=start, end=end, Creator=username)
        gaps = timetool.fillGaps(result)
        sumhours = timetool.countHours(result)
        return {'sumhours': sumhours, 'gaps': gaps}

    def groupedtasks(self, username):
        etool = self.extropytool()
        brains = etool.trackingQuery(
            self.context,
            portal_type=['ExtropyActivity', 'Contract'],
            getResponsiblePerson=[username, 'all'],
            review_state=etool.getOpenStates(),
            sort_on='getProjectTitle')

        customers = etool.dictifyBrains(brains, 'getProjectTitle').items()
        # [('Customer name', [<brain object at ...>]), ...]

        def _key(value):
            return value.Title

        result = OrderedDict()
        for label, raw_contracts in sorted(customers):
            result[label] = []
            contracts = list(raw_contracts)
            contracts.sort(key=_key)
            for c in contracts:
                if c.portal_type == 'Contract':
                    # Contract can have multiple work types
                    obj = c.getObject()
                    work_types = obj.getUniqueWork_types()
                    title = c.Title + ' — ' + work_types[0]
                    result[label].append({'Title': title, 'UID': c.UID})
                    if len(work_types) > 1:
                        for w in work_types[1:]:
                            title = ' ➝ ' + w
                            result[label].append(
                                {'Title': title, 'UID': c.UID})
                else:
                    result[label].append({'Title': c.Title, 'UID': c.UID})

        return result.iteritems()

    def process(self):
        context = self.context
        request = self.request

        records = request.get('hours', [])
        timetool = self.timetool()
        extropytool = self.extropytool()

        # From the form
        date = DateTime(request.get('date'))

        added = []
        last_task = None
        for r in records:
            if r.task and r.start and r.end:
                start = DateTime('%s %s' % (date, r.start))
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
                    last_task = r.task
        if added:
            message = u"Added workhours to " + u", ".join(added)
        else:
            if not added:
                message = u"Changed timespan"
            else:
                message = u"No hours added"

        context.plone_utils.addPortalMessage(message)

        url = context.absolute_url()
        url = url + '/@@timesheet'
        query = date.Date()
        if last_task:
            query += '&' + 'last_task=' + str(last_task)
        return url + '?date=' + query
