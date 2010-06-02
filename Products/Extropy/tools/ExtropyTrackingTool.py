from math import floor
from types import StringTypes, DictType

from zope.interface import implements

from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import search_zcatalog
from Acquisition import aq_base
from App.class_init import InitializeClass
from DateTime import DateTime
from Products.CMFCore.utils import _getAuthenticatedUser
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.ZCatalog import ZCatalog

from Products.Extropy import config
from Products.Extropy import permissions
from Products.Extropy.config import OPEN_STATES
from Products.Extropy.config import TASK_PRIORITIES
from Products.Extropy.interfaces import IExtropyTracking, IExtropyTrackingTool
from Products.Extropy.odict import OrderedDict


class ExtropyTrackingTool(CatalogTool):
    """A tool for tracking tasks and similar things
    """

    id = config.TOOLNAME
    meta_type = config.TOOLTYPE

    security = ClassSecurityInfo()

    implements(IExtropyTrackingTool)

    manage_options = (
        CatalogTool.manage_options
    )

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

    security.declarePublic( 'localQuery' )
    def localQuery(self,node,REQUEST=None, **kw):
        """ a placeful query for tasks"""
        kw['path'] = '/'.join(node.getPhysicalPath())
        return ZCatalog.searchResults(self, REQUEST, **kw)

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
            if IExtropyTracking.providedBy(o):
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
        d = OrderedDict()
        for b in brains:
            newkey = b[key]
            if newkey in d:
                d[newkey].append(b)
            else:
                d[newkey] = [b]
        return d

    # *******************************************************************
    # INSTALLATION OF INDEXES STUFF

    security.declarePublic( 'enumerateIndexes' )
    def enumerateIndexes( self ):
    #   Return a list of ( index_name, type ) pairs for the initial index set.
        return  ( ('UID'            , 'FieldIndex',     None)
                , ('Creator'        , 'FieldIndex',     None)
                , ('SearchableText' , 'ZCTextIndex',    None)
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
                , ('getProjectTitle', 'FieldIndex', 'getProjectTitle')
                , ('getResponsiblePerson', 'KeywordIndex',None)
                , ('start'          , 'DateIndex',      None)
                , ('end'            , 'DateIndex',      None)
                , ('getNosy'        , 'KeywordIndex',   None)
                , ('startendrange'  , 'DateRangeIndex', {'since_field':'start', 'until_field':'end'})
                , ('featureUID', 'FieldIndex', None)
                , ('getInvoiceNumber', 'FieldIndex', None)
                , ('getPriority', 'FieldIndex', None)
                , ('getWorkedHours', 'FieldIndex', None)
                , ('getDueDate','FieldIndex', None)
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
               , 'getId'
               , 'getInvoiceNumber',
               , 'getResponsiblePerson'
               , 'featureUID'
               , 'start'
               , 'end'
               , 'getPriority'
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
