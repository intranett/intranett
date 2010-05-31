from types import StringTypes

from zope.interface import implements

from AccessControl import getSecurityManager
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import search_zcatalog
from Acquisition import aq_base
from App.class_init import InitializeClass
from DateTime import DateTime
from Products.CMFCore.utils import _getAuthenticatedUser
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.CMFPlone.utils import _createObjectByType
from Products.ZCatalog.ZCatalog import ZCatalog

from Products.Extropy import config
from Products.Extropy.interfaces import IExtropyTimeTrackingTool
from Products.Extropy.permissions import VIEW_PERMISSION


class ExtropyTimeTrackerTool(CatalogTool):
    """Extropy's tool for tracking and reporting work-hours
    """

    id = config.TIMETOOLNAME
    meta_type = config.TIMETOOLTYPE

    security = ClassSecurityInfo()

    implements(IExtropyTimeTrackingTool)

    manage_options = (CatalogTool.manage_options)

    security.declareProtected(VIEW_PERMISSION, 'convertHours')
    def convertHours(self, hours):
        """convert a float or an integer hours to a proper datetime amount"""
        return (1.0 / 24.0) * hours

    security.declareProtected(VIEW_PERMISSION, 'getLastRegisteredTime')
    def getLastRegisteredTime(self):
        """get the end of the last registerd hour of today,
           so that we may add more immediately following it
           This query should be global for the current user
        """
        today = DateTime().earliestTime()
        hours= self.getHours(node=None, start=today, end=None, REQUEST=None, Creator=getSecurityManager().getUser().getUserName())
        if not hours:
            return None
        return hours[-1].end

    security.declareProtected(VIEW_PERMISSION, 'getDefaultStartTime')
    def getDefaultStartTime(self):
        """the default start time for today"""
        return self.getLastRegisteredTime() or ( DateTime().earliestTime() + (1.0/24.0)*9.0 )

    security.declareProtected(VIEW_PERMISSION, 'addTimeTrackingHours')
    def addTimeTrackingHours(self, obj, title, hours=0, start=None, end=None):
        """ Add a trackhour to the passed in object """

        # if this object does not have an hourglass already, we just set one.
        if not 'hourglass' in obj.objectIds():
            _createObjectByType('ExtropyHourGlass', obj, 'hourglass')
        hourglass = obj.hourglass

        if hours and end:
            raise ValueError('Cannot define both hours and end')

        if not start:
            start = self.getDefaultStartTime()

        if not end:
            end = start
            if hours:
                end += self.convertHours(hours)

        newid = self.generateUniqueId('workedhours')
        return _createObjectByType('ExtropyHours', hourglass, newid,
                                   title=title, startDate=start, endDate=end)

    security.declareProtected(VIEW_PERMISSION, 'findTimeTrackableParent')
    def findTimeTrackableParent(self, context):
        """ find the next parent of context that can have timetracking"""
        for o in list(context.aq_chain):
            if hasattr(o,'meta_type') and o.meta_type in config.BILLABLE_TYPES:
                return o
        return None

    def _listAllowedRolesAndUsers(self, user):
        """Makes sure the list includes the user's groups.
        """
        result = list(user.getRoles())
        if hasattr(aq_base(user), 'getGroups'):
            result = result + ['user:%s' % x for x in user.getGroups()]
        result.append('Anonymous')
        return result

    security.declareProtected(search_zcatalog, 'searchResults')
    def searchResults(self, REQUEST=None, **kw):
        return ZCatalog.searchResults(self, REQUEST, **kw)

    __call__ = searchResults

    security.declareProtected(VIEW_PERMISSION, 'localQuery')
    def localQuery(self, node=None, REQUEST=None, **kw):
        """ a placeful query for tasks"""
        if node is not None:
            kw[ 'path' ] = '/'.join(node.getPhysicalPath())
        return ZCatalog.searchResults(self, REQUEST, **kw)

    security.declareProtected(VIEW_PERMISSION, 'getHours')
    def getHours(self, node=None, start=None, end=None, REQUEST=None, **kw):
        """ get the hour objects local to an object and between start and endtimes """
        #if node is not None:
        #    kw['path' ] = '/'.join(node.getPhysicalPath())
        if start is not None and end is not None:
            kw['start' ] = {'query' : [start, end ],
                            'range' : 'minmax' }
        elif start is not None and end is None:
            kw['start' ] = {'query' : start,
                            'range' : 'min' }
        elif end is not None and start is None:
            kw['start' ] = {'query' :  end ,
                            'range' : 'max' }

        kw[ 'portal_type'] = 'ExtropyHours'
        kw[ 'sort_on' ]   = 'start'
        return self.localQuery(node=node, REQUEST=REQUEST, **kw)

    security.declareProtected(VIEW_PERMISSION, 'countIntervalHours')
    def countIntervalHours(self, node=None, start=None, end=None, REQUEST=None, **kw):
        """return the number of hours in a specified interval"""
        hours = self.getHours(node=node, start=start, end=end , REQUEST=REQUEST, **kw)
        return self.countHours(hours)

    security.declareProtected(VIEW_PERMISSION, 'countHours')
    def countHours(self, hours):
        """ count the total amount of hours in a sequence of hours-records """
        return sum(h.workedHours for h in hours)

    # These are part of tesdal's view-ish report things.

    security.declareProtected(VIEW_PERMISSION, 'fillGaps')
    def fillGaps(self, events, start=None, end=None):
        # Can add sanity checks to make sure all events are in the same day
        # Set up a tuple of time,[start|end],event where start=0 and end=1
        # sort the list
        # run through the list and detect overlap
        # END is 0 to make sure we don't have overlap accidents when sorting
        END = 0
        NODURATION = 1
        START = 2
        eventslist = []
        for event in events:
            # Handle None as start and end?
            s = event.start
            if callable(s):
                s = s()
            e = event.end
            if callable(e):
                e = e()
            if s.equalTo(e):
                eventslist.append((int(s.timeTime()),NODURATION,event))
            else:
                eventslist.append((int(s.timeTime()),START,event))
                eventslist.append((int(e.timeTime()),END,event))

        # Custom comparator due to Zope bug - don't cmp the brains themselves
        # http://zwiki.org/1145TypeErrorMybrainsCmpXYRequiresYToBeAMybrainsNotAImplicitAcquirerWrapperWithZope281
        # http://www.zope.org/Collectors/Zope/1884
        eventslist.sort(lambda x,y: cmp(x[0:2],y[0:2]))

        # Dict generator, returns a list of dicts
        from math import floor
        def padding(s, e):
            # No padding if start equals end
            if s.equalTo(e): return []
            # Split by the hour
            starthour = s.hour()
            gap = int(floor((e-s)*24))
            hours = []
            if gap:
                for hour in xrange(starthour, starthour+gap):
                    hours.append({'start':'%02d:00' % hour, 'end':'%02d:00' % (hour+1)})
            else:
                hours.append({'start':s.TimeMinutes(), 'end':e.TimeMinutes()})
            return hours


        # Short circuit if no events
        if not eventslist and start is not None and end is not None:
            return padding(start, end)

        # Now we have the sorted events list, and can check the start and end times,
        # and fill in the gaps with dicts.
        events = []
        currentevents = {} # UID:object
        previousevent = None
        for t,s,event in eventslist:
            UID = event.UID
            if callable(UID):
                UID = UID()
            if s == START or s == NODURATION:
                eventstart = event.start
                if callable(eventstart):
                    eventstart = eventstart()
                currentcount = len(currentevents.keys())
                offset = 0

                # The offset is the lowest number available - doesn't make sense to have more than 10
                if currentcount:
                    offsetmap = dict.fromkeys(currentevents.values())
                    for offset in xrange(0,10):
                        if not offsetmap.has_key(offset):
                            break
                #event.setOffset(offset) # Need to mark offset somehow?
                # XXX if no events and gap between event.start and start, add dicts
                if not events and start is not None and not start.equalTo(eventstart):
                    events.extend(padding(start, eventstart))
                # XXX If no currentevents, check gap between previous.end and this.start, add dicts if necessary
                if events and not currentcount and previousevent:
                    previousend = previousevent.end
                    if callable(previousend):
                        previousend = previousend()
                    events.extend(padding(previousend, eventstart))
                events.append(event)
                # USED FOR DEBUGGING
                #events.append((currentcount, offset, event))
                # Add to keyed results

                if s == START:
                    currentevents[UID] = offset
            elif s == END:
                del currentevents[UID]
                previousevent = event
        # XXX Add trailing gap fillers
        if events and previousevent is not None and end is not None:
            previousend = previousevent.end
            if callable(previousend):
                previousend = previousend()
            # XXX end can be before previousend - catch that case
            if not end.equalTo(previousend):
                events.extend(padding(previousend, end))
        return events

    security.declarePublic( 'enumerateIndexes' )
    def enumerateIndexes( self ):
    #   Return a list of ( index_name, type ) pairs for the initial index set.
        return  ( ('Creator'        , 'FieldIndex', None)
                , ('SearchableText' , 'ZCTextIndex', None)
                , ('created'        , 'DateIndex', None)
                , ('modified'       , 'DateIndex', None)
                , ('allowedRolesAndUsers', 'KeywordIndex', None)
                , ('review_state'   , 'FieldIndex', None)
                , ('meta_type'      , 'FieldIndex', None)
                , ('getId'          , 'FieldIndex', None)
                , ('path'           , 'PathIndex' , None)
                , ('portal_type'    , 'FieldIndex', None)
                , ('getProjectTitle', 'FieldIndex', 'getProjectTitle')
                , ('getResponsiblePerson', 'FieldIndex', 'getResponsiblePerson')
                , ('start'      , 'DateIndex',      None)
                , ('end'        , 'DateIndex',      None)
                , ('nosy'       , 'KeywordIndex',   None)
                , ('workedHours', 'FieldIndex',     None)
                , ('getBudgetCategory','FieldIndex',None)
                , ('UID','FieldIndex',None)
                )

    security.declarePublic( 'enumerateColumns' )
    def enumerateColumns( self ):
        #   Return a sequence of schema names to be cached.
        return ( 'Subject'
               , 'Title'
               , 'Description'
               , 'Type'
               , 'review_state'
               , 'Creator'
               , 'getIcon'
               , 'created'
               , 'modified'
               , 'CreationDate'
               , 'EffectiveDate'
               , 'ExpiresDate'
               , 'ModificationDate'
               , 'portal_type'
               , 'getResponsiblePerson'
               , 'getId'
               , 'start'
               , 'end'
               , 'workedHours'
               , 'getBudgetCategory'
               , 'getProjectTitle'
               , 'getPackageTitle'
               , 'UID')

    def _initIndexes(self):
        """Set up indexes and metadata, as enumared by enumerateIndexes() and
        enumerateColumns (). Subclasses can override these to inject additional
        indexes and columns.
        """

        class Record:
            """ a moron simple object for carrying the 'extra'-payload to index
            constructors
            """
            def __init__(self, **kw):
                self.__dict__.update(kw)

        addIndex = self.addIndex
        addColumn = self.addColumn

        # Content indexes
        self._catalog.indexes.clear()
        for (index_name, index_type, extra) in self.enumerateIndexes():
            if extra is None:
                addIndex( index_name, index_type)
            else:
                if isinstance(extra, StringTypes):
                    p = Record(indexed_attrs=extra)
                elif isinstance(extra, dict):
                    p = Record(**extra)
                else:
                    p = Record()

                addIndex( index_name, index_type, extra=p )

        # Cached metadata
        self._catalog.names = ()
        self._catalog.schema.clear()
        for column_name in self.enumerateColumns():
            addColumn( column_name )


InitializeClass(ExtropyTimeTrackerTool)
