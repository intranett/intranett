from itertools import groupby
from operator import attrgetter

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.Extropy import config
from Products.Extropy import permissions
from Products.Extropy.config import *

from Products.CMFPlone.CatalogTool import CatalogTool
from Products.Extropy.interfaces import IExtropyTracking, IExtropyTrackingTool

from types import StringTypes, DictType

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.Five.traversable import Traversable

from DateTime import DateTime
from math import floor

class ExtropyTrackingTool(CatalogTool):
    """A tool for tracking tasks and similar things
    """

    id = config.TOOLNAME
    meta_type = config.TOOLTYPE

    security = ClassSecurityInfo()

    __implements__ = (CatalogTool.__implements__, IExtropyTrackingTool)

    manage_options = (
        CatalogTool.manage_options
    )

    def __setstate__(self, state):
        CatalogTool.__setstate__(self, state)
        self._catalog.useBrains(Traversable)

    # a method to get placeful task results
    security.declarePublic( 'localQuery' )
    def localQuery(self,node,REQUEST=None, **kw):
        """ a placeful query for tasks"""
        kw[ 'path' ] = '/'.join(node.getPhysicalPath())
        return apply(CatalogTool.searchResults, (self, REQUEST), kw)

    security.declareProtected(permissions.VIEW_PERMISSION, 'trackingQuery')
    def trackingQuery(self, node, REQUEST=None, **kw):
        """  does a local query from the nearest parent that implements IExtropyTracking"""
        node = self.getQueryAnchor(node)
        return self.localQuery(node, REQUEST, **kw)

    security.declareProtected(permissions.VIEW_PERMISSION, 'getOpenStates')
    def getOpenStates(self, objecttype=None):
        """ the names of workflowstates we consider 'open' """
        return config.OPEN_STATES

    security.declareProtected(permissions.VIEW_PERMISSION, 'getQueryAnchor')
    def getQueryAnchor(self, context, metatype=None):
        """Gets the containg parent of context, if it is an ExtropyBase object, or the first on that is.
        """
        for o in list(context.aq_chain):
            if IExtropyTracking.isImplementedBy(o):
                if metatype is None:
                    return o
                elif hasattr(o,'meta_type') and metatype == o.meta_type:
                    return o
        return getToolByName(self, 'portal_url').getPortalObject()

    security.declareProtected(permissions.VIEW_PERMISSION, 'dictifyResults')
    def dictifyResults(self, results, key):
        """create a dict from the hours so we can separate them by key"""
        d={}
        for h in results:
            newkey = h[key]
            if d.has_key(newkey):
                d[newkey].append(h)
            else:
                d[newkey]=[h]
        return d

    security.declareProtected(VIEW_PERMISSION, 'countEstimates')
    def countEstimates(self, objects):
        """ count the estimates of many records """
        if objects is None or len(objects)==0 or not objects:
            return 0
        return reduce(lambda x, y: x + y , [h.getEstimatedDuration for h in objects])

    # *******************************************************************
    # VOCABULARY METHODS
    #

    security.declareProtected(permissions.VIEW_PERMISSION, 'getOpenWorkflowStates')
    def getOpenWorkflowStates(self):
        """the workflow states that are classified as open"""
        return OPEN_STATES


    security.declareProtected(permissions.VIEW_PERMISSION, 'getPriorityVocabulary')
    def getPriorityVocabulary(self):
        """Shows the priorities."""
        return TASK_PRIORITIES

    security.declareProtected(permissions.VIEW_PERMISSION, 'getPriorityDescription')
    def getPriorityDescription(self, priority):
        """Gets the priority description."""
        for i in TASK_PRIORITIES:
            if str(i[0]) == str(priority):
                return i[1]
        return 'None'

    security.declareProtected(permissions.VIEW_PERMISSION, 'getTaskEstimatesVocabulary')
    def getTaskEstimatesVocabulary(self):
        """Show the task estimates."""
        return TASK_ESTIMATES

    security.declareProtected(permissions.VIEW_PERMISSION, 'getTaskEstimateDescription')
    def getTaskEstimateDescription(self, value):
        """Gets the textsting describing the estimate."""
        for i in TASK_ESTIMATES:
            if str(i[0]) == str(value):
                return i[1]
        return 'Not set'


    def sumEstimates(self, tasks):
        """ sums the total amount of estimated hours in a sequence of tasks """
        if tasks is None or len(tasks)==0 or not tasks:
            return 0
        return reduce(lambda x, y: x + y , [t.getEstimatedDuration for t in tasks])


    security.declareProtected(permissions.VIEW_PERMISSION, 'getFullnameOf')
    def getFullnameOf(self, username):
        """Returns the fullname from a username."""
        membershiptool = getToolByName(self, 'portal_membership')
        member = membershiptool.getMemberById(username)
        if member is None:
            return username
        else:
            return member.getProperty('fullname')

    security.declareProtected(permissions.VIEW_PERMISSION, 'howLongAgo')
    def howLongAgo(self, date):
        """Returns a nice printed display of how long ago something
        happened.
        """
        now = DateTime()
        d = now - date
        days =  int(floor(d))
        return days

    security.declareProtected(permissions.VIEW_PERMISSION, 'dictifyBrains')
    def dictifyBrains(self, brains, key):
        """create a dict from the brains so we can separate them by key"""
        d={}
        for b in brains:
            newkey = b[key]
            if d.has_key(newkey):
                d[newkey].append(b)
            else:
                d[newkey]=[b]
        return d

    def dictifyTasksByDate(self, tasks, fill=True, startdate=None, enddate=None):
        """create a dict from the tasks so we can separate them by Dates"""
        d={}
        for h in tasks:
            newkey = h.start.earliestTime()
            if d.has_key(newkey):
                d[newkey].append(h)
            else:
                d[newkey]=[h]
        alldates = d.keys()
        if fill and alldates:
            end = (enddate or max(alldates)).earliestTime()
            start = (startdate or min(alldates)).earliestTime()
            diff = int(end-start)
            for i in range(0,diff):
                if not d.has_key(start+i):
                    d[start+i]=[]
        return d


    security.declareProtected(permissions.VIEW_PERMISSION, 'getDeliverablesWithTasks')
    def getDeliverablesWithTasks(self,context):
        """get deliverables with nested tasks"""
        # expand the brains schema to allow for setting 'children'
        rschema = self._catalog._v_result_class.__record_schema__
        rschema['children'] = len(self.schema()) + 3

        objects = list(self.trackingQuery(
            context, meta_type=('ExtropyTask', 'ExtropyFeature')))
        objects.sort(key=lambda b: b.getPath())

        deliverables = []
        for dtitle, ditems in groupby(objects,
                                      attrgetter('getDeliverableTitle')):
            deliverable = ditems.next()
            deliverable.children = tuple(ditems)
            deliverables.append(deliverable)

        deliverables.sort(key=attrgetter('review_state'))
        bystate = dict((k, tuple(v))
                       for (k, v) in groupby(deliverables,
                                             attrgetter('review_state')))
        order = ('open', 'taskscomplete', 'testing', 'planned', 'prospective',
                 'closed', 'discarded')
        for state in order:
            deliverables = bystate.pop(state, ())
            for deliverable in deliverables:
                yield deliverable

    # *******************************************************************
    # INSTALLATION OF INDEXES STUFF

    security.declarePublic( 'enumerateIndexes' )
    def enumerateIndexes( self ):
    #   Return a list of ( index_name, type ) pairs for the initial index set.
        return  ( ('UID'            , 'FieldIndex',     None)
                , ('Creator'        , 'FieldIndex',     None)
                , ('SearchableText' , 'TextIndex',      None)
                , ('Subject'        , 'KeywordIndex',   None)
                , ('created'        , 'DateIndex',      None)
                , ('modified'       , 'DateIndex',      None)
                , ('allowedRolesAndUsers', 'KeywordIndex', None)
                , ('review_state'   , 'FieldIndex',     None)
                , ('meta_type'      , 'FieldIndex',     None)
                , ('getId'          , 'FieldIndex',     None)
                , ('path'           , 'PathIndex' ,     None)
                , ('portal_type'    , 'FieldIndex',     None)
                , ('getParticipants', 'KeywordIndex',   None)
                , ('getResponsiblePerson', 'KeywordIndex',None)
                , ('start'          , 'DateIndex',      None)
                , ('end'            , 'DateIndex',      None)
                , ('getNosy'        , 'KeywordIndex',   None)
                , ('startendrange'  , 'DateRangeIndex', {'since_field':'start', 'until_field':'end'})
                , ('featureUID'     , 'FieldIndex',     None)
                , ('getPriority'     , 'FieldIndex',    None)
                , ('getEstimatedDuration','FieldIndex', None)
                , ('getRemainingTime','FieldIndex',     None)
                , ('getWorkedHours','FieldIndex',     None)
                , ('getDueDate','FieldIndex',     None)
                )

    security.declarePublic( 'enumerateColumns' )
    def enumerateColumns( self ):
        #   Return a sequence of schema names to be cached.
        return ( 'UID'
               , 'Title'
               , 'Description'
               , 'Subject'
               , 'Type'
               , 'review_state'
               , 'Creator'
               , 'getIcon'
               , 'created'
               , 'effective'
               , 'expires'
               , 'modified'
               , 'CreationDate'
               , 'EffectiveDate'
               , 'ExpiresDate'
               , 'ModificationDate'
               , 'portal_type'
               , 'getResponsiblePerson'
               , 'getRemainingTime'
               , 'getId'
               , 'featureUID'
               , 'start'
               , 'end'
               , 'getPriority'
               , 'getEstimatedDuration'
               , 'getDueDate'
               , 'getWorkedHours'
               , 'getProjectTitle'
               , 'getPhaseTitle'
               , 'getDeliverableTitle'
               , 'countOpenTasks'
               , 'countTasks'
               )


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

        base = aq_base(self)
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
                elif isinstance(extra, DictType):
                    p = Record(**extra)
                else:
                    p = Record()
                addIndex( index_name, index_type, extra=p )

        # Cached metadata
        self._catalog.names = ()
        self._catalog.schema.clear()
        for column_name in self.enumerateColumns():
            addColumn( column_name )


InitializeClass(ExtropyTrackingTool)
