from zope import interface
from Products import Five
from DateTime import DateTime
from Products.CMFCore import utils as cmf_utils
from Products.Extropy.utils import activity

# BBB DateTime < 3
try:
    from DateTime.DateTime import _MONTHS
except ImportError:
    _MONTHS = DateTime._months


# Iterators used by the view
# We use custom iterators because we need extra data (total)
# and ordering (which is different depending on type)
# And the ability to print some data differently (month 12 is December)
class ReportKey:
    def __init__(self, key, data=None):
        self.keyname = str(key)
        if key == 'activity' and data is not None:
            self.key = activity(data)
        elif data is None:
            self.key = key
        else:
            nodekey = data
            if isinstance(key, basestring):
                for k in key.split('/'):
                    nodekey = getattr(nodekey, k)
            if callable(nodekey):
                nodekey = nodekey()
            self.key = nodekey

    def __hash__(self):
        # XXX Add mutable check somewhere
        return hash(self.key)

    def __cmp__(self, other):
        if isinstance(other, (int, basestring, tuple, DateTime)):
            return cmp(self.key, other)
        return cmp(self.key, other.key)

    def __str__(self):
        if self.keyname == 'hoursBillable':
            if self.key:
                return 'Billable'
            else:
                return 'Not billable'
        if self.keyname.endswith('week'):
            return 'Week %s' % self.key
        if self.keyname.endswith('month'):
            return _MONTHS[self.key]
        if not isinstance(self.key, basestring):
            return str(self.key)
        return self.key

    def __unicode__(self):
        return str(self).decode('utf-8')


def iteratorFactory(key, parent=None):
    return ReportIterator(key, parent)


class ReportIterator:
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, key, parent=None):
        self._data = {}
        self._keys = []
        self.pos=0
        self.key = key
        self.value = 0
        self.parent = parent

    def __iter__(self):
        self.reset()
        if not getattr(self, '_sorted', False):
            self._keys.sort()
            self._sorted = True
        return self

    def next(self):
        if self.pos < self._getUpper():
            self.pos += 1
            return self._data[self._keys[self.pos-1]]
        raise StopIteration, 'Reached upper bounds'

    def _getUpper(self):
        return len(self._keys)

    def hasData(self):
        return not not len(self._keys)

    def dataHasData(self):
        return not not [x for x in self._data.values() if x.hasData()]

    def getParent(self):
        return self.parent

    def getBreadCrumb(self):
        output = []
        parent= self
        while parent is not None:
            output.append(str(parent.getKey()))
            parent = parent.getParent()
        output.reverse()
        return ' - '.join(output[1:]) # Chop off the 'Total'

    def add(self, keys, item):
        # This should have the data building methods
        if hasattr(item, 'workedHours'):
            self.value += item.workedHours

    def get(self, *args, **kwargs):
        return self._data.get(*args, **kwargs)

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        if not self._data.has_key(key):
            self._keys.append(key)
        return self._data.__setitem__(key, value)

    def __delitem__(self, key):
        self._keys.remove(key)
        return self._data.__delitem__(key)

    def getSortKey(self):
        return self.key

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

    def reset(self):
        self.pos = 0

    def __str__(self):
        return '%s: %s' % (self.getKey(), self.getValue())


class IReportView(interface.Interface):
    def getReportData():
        """Return report data.
        """


class ReportView(Five.BrowserView):
    """Hour report
    """

    def __init__(self, context, request):
        Five.BrowserView.__init__(self, context, request)

        self.portal_membership = cmf_utils.getToolByName(self.context,
                                                         'portal_membership')
        self.extropy_tracking_tool = cmf_utils.getToolByName(self.context,
                                                         'extropy_tracking_tool')
        self.extropy_timetracker_tool = cmf_utils.getToolByName(self.context,
                                                                'extropy_timetracker_tool')

    def getPhysicalPath(self):
        return self.context.getPhysicalPath()

    # XXX
    # Make a result type that is aware of datatypes, sorting and printing
    # Especially dates - when grouping on month, sort (instead of string sort)
    # and enable printing of month name instead of number
    def getReportData2(self, start=None, end=None, username=None, group_by=None, **query):
        """Get the report data"""
        if group_by is None:
            group_by = ['Creator', 'getBudgetCategory']
        if isinstance(group_by, basestring):
            group_by = group_by.split(':')
        if not query.has_key('portal_type'):
            query['portal_type']='ExtropyHours'

        if start is not None or end is not None:
            if start is None:
                start = DateTime('2000/01/01')
            if end is None:
                end = DateTime()
            query['start'] = {'query' : (start,end) ,
                              'range' : 'minmax'}
        if username is not None:
            query['Creator'] = username

        def processHourEntry(dct, keys, hour):
            workedHours = hour.workedHours
            dct['total'] = dct.get('total', 0) + workedHours
            if keys:
                key = keys[0]
                dctkey = hour
                for k in key.split('/'):
                    dctkey = getattr(dctkey, k)
                if callable(dctkey):
                    dctkey = dctkey()
                if not isinstance(dctkey, basestring):
                    dctkey = str(dctkey)
                newdict = dct.get(dctkey, None)
                if newdict is None:
                    newdict = {}
                newdict = processHourEntry(newdict, keys[1:], hour)
                dct[dctkey] = newdict
            return dct

        hours = self.extropy_timetracker_tool.searchResults(**query)
        result = {}
        #print DateTime()
        for h in hours:
            result = processHourEntry(result, group_by, h)
        return result

    def getReportData(self, node=None, start=None, end=None, username=None, group_by=None, **query):
        """Get the report data"""
        if group_by is None:
            group_by = ['Creator', 'getBudgetCategory']
        if isinstance(group_by, basestring):
            group_by = group_by.split(':')
        if not query.has_key('portal_type'):
            query['portal_type']='ExtropyHours'
        if query.has_key('local'):
            query['path'] = '/'.join(self.context.getPhysicalPath())

        if start or end:
            if not start:
                start = DateTime('2000/01/01')
            if not end:
                end = DateTime()
            query['start'] = {'query' : (start,end) ,
                              'range' : 'minmax'}
        if username is not None:
            query['Creator'] = username

        def processHourEntry(node, keys, hour):
            node.add(keys, hour)
            if keys:
                key = keys[0]
                nodekey = ReportKey(key, hour)
                newnode = node.get(nodekey, None)
                if newnode is None:
                    newnode = iteratorFactory(nodekey, parent=node)
                newnode = processHourEntry(newnode, keys[1:], hour)
                node[nodekey] = newnode
            return node

        hours = self.extropy_timetracker_tool.searchResults(**query)
        rootnode = iteratorFactory('Total')
        for h in hours:
            rootnode = processHourEntry(rootnode, group_by, h)
        return rootnode


class ColIterator:
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, tabledata, rowiterator, pos):
        self.data = tabledata
        self.rows = rowiterator
        self.pos = 0
        self.rowpos = pos
        self.upper = len(self.data._cols)

    def __iter__(self):
        self.reset()
        return self

    def next(self):
        if self.pos < self.upper:
            self.pos += 1
            return self.value()
        raise StopIteration, 'Reached upper bounds'

    def header(self):
        return self.data._cols[self.pos-1]

    def value(self):
        return self.data._data.get(self.data._rows[self.rowpos-1] + (self.data._cols[self.pos-1],),0)

    def reset(self):
        self.pos = 0

    def rowheader(self):
        rh = self.data._rows[self.rowpos-1]
        if not isinstance(rh, (list,tuple)):
            return rh,
        else:
            return rh

    def __str__(self):
        return str(self.data._cols[self.pos-1])


class RowIterator:
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, tabledata):
        self.data = tabledata
        self.pos=0
        self.upper = len(self.data._rows)

    def __iter__(self):
        self.reset()
        return self

    def next(self):
        if self.pos < self.upper:
            self.pos += 1
            return ColIterator(self.data, self, self.pos)
        raise StopIteration, 'Reached upper bounds'

    def reset(self):
        self.pos = 0

    def __str__(self):
        return '%s' % self.data._rows[self.pos-1]


class TableData:
    """Table data structure providing iterators for cols and rows"""
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, keys, brains):
        self.pos=0
        data = {} # Keeping data itself
        cols = {} # Keeping col keys
        rows = {} # Keeping row keys
        rkeys,ckey = keys[:-1],keys[-1]
        for brain in brains:
            hours = brain.workedHours
            colkey = ReportKey(ckey, brain)
            cols[colkey] = 1
            rowkeys = tuple([ReportKey(row, brain) for row in rkeys])
            rows[rowkeys] = 1
            datakey = rowkeys + (colkey,)
            value = data.get(datakey, 0)
            value += hours
            data[datakey] = value
        self._data = data
        self._cols = cols.keys()
        self._cols.sort()
        self._rows = rows.keys()
        self._rows.sort()

    def getColHeaders(self):
        return self._cols

    def getRowHeaders(self):
        return self._rows

    def rows(self):
        return RowIterator(self)

    # HTML helpers that should be in view or something
    def getTableHeaders(self):
        if len(self.getRowHeaders()) == 1:
            return [str(x) for x in self.getColHeaders()]
        else:
            return [rh.keyname for rh in self.getRowHeaders()[0]] + [str(x) for x in self.getColHeaders()]


class TableView(ReportView):
    """Hour report
    """

    def getReportData(self, node=None, start=None, end=None, username=None, group_by=None, **query):
        """Get the report data"""
        if group_by is None:
            group_by = ['Creator', 'getBudgetCategory']
        if isinstance(group_by, basestring):
            group_by = group_by.split(':')

        if not query.has_key('portal_type'):
            query['portal_type']='ExtropyHours'

        if query.has_key('local'):
            query['path'] = '/'.join(self.context.getPhysicalPath())

        if start or end:
            if not start:
                start = DateTime('2000/01/01')
            if not end:
                end = DateTime()
            query['start'] = {'query' : (start,end) ,
                              'range' : 'minmax'}
        if username is not None:
            query['Creator'] = username

        hours = self.extropy_timetracker_tool.searchResults(**query)


        data = TableData(group_by, hours)
        return data

class CSVView(TableView):
    """Hour report
    """

    def __call__(self):
        reqget = self.request.get
        query = {}
        for key in ['review_state','portal_type','getBudgetCategory']:
            v = reqget(key, None)
            if v is not None:
                query[key] = v
        if reqget('local'):
            query['path'] = '/'.join(self.context.getPhysicalPath())
        group_by = reqget('group_by', 'activity:getBudgetCategory')
        if not isinstance(group_by, (list, tuple)):
            group_by = group_by.split(':')
        data = self.getReportData(start=reqget('start', None), 
                                  end=reqget('end', None), 
                                  username=reqget('username', None), 
                                  group_by=group_by, 
                                  **query)
        self.request.response.setHeader('Content-Type', 'text/csv; charset="utf-8"')
        out = []
        if len(data.getRowHeaders()) == 1:
            out.append(','.join([str(x) for x in data.getColHeaders()]))
            for row in data.rows():
                out.append(','.join([str(col) for col in row]))
        else:
            out.append(','.join([rh.keyname for rh in data.getRowHeaders()[0]] + [str(x) for x in data.getColHeaders()]))
            for row in data.rows():
                out.append(','.join([str(r) for r in row.rowheader()] + [str(col) for col in row]))
        return '\n'.join(out)
