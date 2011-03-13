from OFS.Cache import Cacheable
from Acquisition import aq_base
from Acquisition import aq_parent
from AccessControl import ClassSecurityInfo
from Shared.DC.Scripts.Script import Script
from Products.PageTemplates.PageTemplate import PageTemplate
from Products.Archetypes.public import *
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import cookString
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import createExprContext

PortletSchema = BaseSchema + Schema((

    StringField('id',
        widget = IdWidget(
            visible = {
                'edit' : 'hidden',
                'view' : 'hidden',
            },
        ),
    ),

    StringField('condition',
        default = 'object/hasPortletData',
        widget = StringWidget(
        ),
    ),

))


class Portlet(BaseContent, Cacheable):
    """A baseclass for Portlets."""

    schema = PortletSchema
    security = ClassSecurityInfo()

    def __call__(self, callingcontext=None):
        """Renders the portlet when called."""
        callingcontext = self.getCallingContext(callingcontext)
        if self.portletVisibilityInContext(callingcontext):
            return self.portlet_wrapper(callingcontext=callingcontext)
        return None

    security.declarePrivate('getCallingContext')
    def getCallingContext(self, callingcontext=None):
        """Gets the calling context."""
        if callingcontext is None:
            callingcontext = aq_parent(self)
        # context might be page template
        if isinstance(callingcontext, (Script,PageTemplate)):
            callingcontext = aq_parent(callingcontext)
        if callingcontext == getToolByName(self, 'portal_portlets'):
            callingcontext = aq_parent(callingcontext)
        return callingcontext

    security.declareProtected(View, 'portletName')
    def portletName(self):
        """Returns a sanitized name for the portlet for use in templates."""
        return cookString(self.Title())

    security.declareProtected(View, 'getPortletEmitter')
    def getPortletEmitter(self):
        """Returns a template to render the contents of the portlet."""
        return self.default_template

    security.declarePublic('portletVisibilityInContext')
    def portletVisibilityInContext(self, context):
        """Evaluates expressions."""
        context = self.getCallingContext(context)
        try:
            if self.condition and context is not None:
                portal = getToolByName(self, 'portal_url').getPortalObject()
                object = self
                __traceback_info__ = (context, portal, object, self.condition)
                ec = createExprContext(context, portal, object)
                return Expression(self.condition)(ec)
            else:
                return 0
        except AttributeError:
            return 0

        return self.hasPortletData()

    security.declareProtected(View, 'getPortletData')
    def getPortletData(self):
        """Makes sure we only fetch the portlet contents once in every request."""
        cachekey = self.UID()
        if self.REQUEST.has_key(cachekey):
#            self.plone_log(self.absolute_url(), 'cache hit in getPortletData %s' % self.getId())
            return self.REQUEST.get(cachekey)

        contents = self._fetchPortletData()

        self.REQUEST.set(cachekey, contents)
        return contents

    security.declareProtected(View, 'hasPortletData')
    def hasPortletData(self):
        """Checks whether we should render at all."""
        return self.getPortletData() and 1 or 0

    def _fetchPortletData(self):
        """Fetchs the main contents of the portlet.

        This one should be overridden for subclasses so that it can easily
        be determined whether to show the portlet or not in context.
        Not to be called directly, call getPortletData.
        """

        return []

    def __url(self):
        """"""
        return '/'.join(self.getPhysicalPath())

    # we force these to catalog themselves in the portlets tool
    security.declareProtected(ModifyPortalContent, 'indexObject')
    def indexObject(self):
        """"""
        pt = getToolByName(self, 'portal_portlets', None)
        pt.catalog_object(self, self.__url())

    security.declareProtected(ModifyPortalContent, 'unindexObject')
    def unindexObject(self):
        """"""
        pt = getToolByName(self, 'portal_portlets', None)
        pt.uncatalog_object(self.__url())
        # Specially control reindexing to UID catalog
        # the pathing makes this needed
        self._uncatalogUID(self)

    security.declareProtected(ModifyPortalContent, 'reindexObject')
    def reindexObject(self, idxs=[]):
        """"""
        if idxs == []:
            if hasattr(aq_base(self), 'notifyModified'):
                self.notifyModified()
        pt = getToolByName(self, 'portal_portlets', None)
        if pt is not None:
            # We want the intersection of the catalogs idxs
            # and the incoming list
            lst = idxs
            indexes = pt.indexes()
            if idxs:
                lst = [i for i in idxs if i in indexes]
            pt.catalog_object(self, self.__url(), idxs=lst)

        # Specially control reindexing to UID catalog
        # the pathing makes this needed
        self._catalogUID(self)


registerType(Portlet)
