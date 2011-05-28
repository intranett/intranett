from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.ZCatalog.Lazy import LazyCat

from Products.Extropy.browser.worklog import DateToPeriod, WorkLogView


class ProjectsListing(BrowserView):

    def customers(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = self.context.getPhysicalPath()
        query = {
            'portal_type': 'Contract',
            'review_state': 'active',
            path: {'path': path},
        }
        contracts = catalog(query)
        etool = getToolByName(self.context, 'extropy_tracking_tool')
        projects = etool.searchResults(
            meta_type=['ExtropyProject'],
            review_state='active',
        )
        brains = LazyCat((contracts, projects))
        # dict of {'title': [{title='', url='', }, ]}
        result = {}
        for b in brains:
            contract = b.getObject()
            total_hours = None
            if 'Management Project' in contract.Subject():
                continue
            if contract.portal_type == 'ExtropyProject':
                customer = contract
            else:
                contract_type = contract.getContract_type()
                if contract_type != 'development':
                    continue
                customer = aq_parent(contract)
                total_hours = contract.getWorkedHours()

            worklog = WorkLogView(contract, self.request)
            worklog.group_by = self.request.get("group_by", "person")
            (worklog.start, worklog.end) = DateToPeriod(
                period=worklog.period, date=worklog.start-1)
            activity = worklog.activity()
            hours = sum([x['summary']['hours'] for x in activity])
            persons = [x['title'] for x in activity]
            if len(persons) > 1:
                persons = "%s and %s" % (", ".join(persons[:-1]), persons[-1])
            else:
                persons = "".join(persons)
            customer_title = customer.Title()
            if customer_title not in result:
                result[customer_title] = []

            result[customer_title].append({
                'url': b.getURL(),
                'title': b.Title,
                'project_manager': contract.getProjectManager(),
                'status': contract.getProjectStatus(),
                'hours': hours,
                'start': worklog.start,
                'end': worklog.end,
                'persons': persons,
                'total': total_hours,
            })
        flatten = []
        def _key(value):
            return value['title']
        for k, v in result.items():
            v.sort(key=_key)
            flatten.append((k, v))
        return sorted(flatten)
