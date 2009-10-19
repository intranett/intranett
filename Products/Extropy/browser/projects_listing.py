from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


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
                data = dict(
                    url=project.absolute_url(),
                    title=project.Title(),
                    project_manager=project.getProjectManager(),
                    status=project.getProjectStatus(),
                )
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
