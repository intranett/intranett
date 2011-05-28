from Acquisition import aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class SupportListing(BrowserView):


    def customers(self):
        timetool = getToolByName(self.context, 'extropy_timetracker_tool')
        year = DateTime().year()
        quarters = {
            1:('%s/01/01'%year,'%s/03/31'%year),
            2:('%s/04/01'%year,'%s/06/30'%year),
            3:('%s/07/01'%year,'%s/09/30'%year),
            4:('%s/10/01'%year,'%s/12/31'%year)}
        quarter = DateTime().month() / 3 + bool(DateTime().month() % 3)
        qstart =DateTime(quarters[quarter][0])
        qend = DateTime(quarters[quarter][1])
        catalog = getToolByName(self.context, 'portal_catalog')
        path = self.context.getPhysicalPath()
        query = {
            'portal_type': 'Contract',
            'review_state': 'active',
            path: {'path': path},
        }
        contracts = catalog(query)
        result = {}
        for b in contracts:
            contract = b.getObject()
            total_hours = None
            contract_type = contract.getContract_type()
            if contract_type != 'support':
                continue
            customer = aq_parent(contract)
            hours = timetool.countIntervalHours(node=contract,start=qstart, end=qend);
            customer_title = customer.Title()
            if customer_title not in result:
                result[customer_title] = []

            result[customer_title].append({
                'url': b.getURL(),
                'title': b.Title,
                'project_manager': contract.getProjectManager(),
                'status': contract.getProjectStatus(),
                'hours': hours,
                'start': qstart,
                'end': qend,
                'total': total_hours,
            })
        flatten = []
        def _key(value):
            return value['title']
        for k, v in result.items():
            v.sort(key=_key)
            flatten.append((k, v))
        return sorted(flatten)
