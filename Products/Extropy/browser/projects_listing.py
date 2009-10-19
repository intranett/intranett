from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Extropy.browser.worklog import DateToPeriod, WorkLogView


class ProjectsListing(BrowserView):
    def projects(self):
        etool = getToolByName(self.context, 'extropy_tracking_tool')
        brains = etool.searchResults(meta_type='ExtropyProject', review_state=['active', 'closable'], sort_on='getId')
        active = dict(title='Active projects', projects=[])
        ongoing = dict(title='Ongoing projects', projects=[])
        internal = dict(title='Internal projects', projects=[])
        closable = dict(title='Finished projects waiting for invoicing', projects=[])
        other = dict(title='Other', projects=[])
        for state, projects in etool.dictifyBrains(brains, 'review_state').iteritems():
            for project in projects:
                project = project.getObject()
                worklog = WorkLogView(project, self.request)
                worklog.group_by = self.request.get("group_by", "person")
                (worklog.start, worklog.end) = DateToPeriod(period=worklog.period, date=worklog.start-1)
                activity = worklog.activity()
                hours = sum([x['summary']['hours'] for x in activity])
                persons = [x['title'] for x in activity]
                data = dict(
                    url=project.absolute_url(),
                    title=project.Title(),
                    project_manager=project.getProjectManager(),
                    status=project.getProjectStatus(),
                    hours=hours,
                    start=worklog.start,
                    end=worklog.end,
                )
                if len(persons) > 1:
                    data['persons'] = "%s and %s" % (", ".join(persons[:-1]), persons[-1])
                else:
                    data['persons'] = "".join(persons)
                if state == 'active':
                    if 'Ongoing Project' in project.Subject():
                        ongoing['projects'].append(data)
                    elif 'Management Project' in project.Subject():
                        internal['projects'].append(data)
                    else:
                        active['projects'].append(data)
                elif state == 'closable':
                    closable['projects'].append(data)
                else:
                    other['projects'].append(data)
        result = [active, ongoing, internal, closable]
        return result
