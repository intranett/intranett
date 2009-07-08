from types import StringTypes

from Acquisition import aq_base, aq_parent, aq_inner
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.Archetypes.config import REFERENCE_CATALOG

from Products.CMFCore.utils import getToolByName

from Products.Extropy.config import *
from Products.Extropy.content.ExtropyBase import ExtropyBase, ExtropyBaseSchema, ParticipantsSchema, TimeSchema, EstimatesSchema
from Products.Extropy.content.ExtropyHistoryTrackable import ExtropyHistoryTrackable

from Products.CMFCore import permissions
from Products.Extropy.permissions import MANAGE_PLAN_ITEMS

from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

from Products.Extropy.interfaces import IExtropyPlan

from DateTime import DateTime


ExtropyPlanSchema = ExtropyBaseSchema.copy() + ParticipantsSchema.copy() + TimeSchema.copy() + Schema((
    ReferenceField('items',
        relationship = PLAN_RELATIONSHIP,
        write_permission = MANAGE_PLAN_ITEMS,
        required = False,
        searchable = False,
        #validators = ('',), # Make sure items are not in completed state
        #allowed_types_method = None, # Do we have a method listing Extropy types?
        widget = ReferenceWidget(
            label = "Items",
            description = "Items on this plan",
            label_msgid = "label_items",
            description_msgid = "help_items",
    )),
    ReferenceField('additionalItems',
        relationship = PLAN_ADDITIONAL_RELATIONSHIP,
        required = False,
        searchable = False,
        #validators = ('',), # Make sure items are not in completed state
        #allowed_types_method = None, # Do we have a method listing Extropy types?
        widget = ReferenceWidget(
            label = "Items",
            description = "Items on this plan",
            label_msgid = "label_items",
            description_msgid = "help_items",
    )),
))


class ExtropyPlan(ExtropyBase, BaseFolder):
    """A plan is a list of deliverables or tasks to be completed in a timespan."""

    schema = ExtropyPlanSchema

    __implements__ = (IExtropyPlan, INonStructuralFolder)

    security = ClassSecurityInfo()

    security.declareProtected(MANAGE_PLAN_ITEMS, 'addItem')
    def addItem(self, item, **kw):
        """ Add item to the plan. Provide target state as keyword to reference"""
        pass

    security.declareProtected(MANAGE_PLAN_ITEMS, 'deleteItem')
    def deleteItem(self, item):
        """ Delete item from the plan"""
        pass

    security.declareProtected(permissions.View, 'getItems')
    def getItems(self):
        """ Get all items on this plan. """
        pass

    security.declareProtected(permissions.ModifyPortalContent, 'addAdditionalItem')
    def addAdditionalItem(self, item, **kw):
        """Add item after approved"""
        pass

    security.declareProtected(permissions.ModifyPortalContent, 'deleteAdditionalItem')
    def deleteAdditionalItem(self, item, **kw):
        """Remove additional item"""
        pass

    security.declareProtected(permissions.View, 'getAdditionalItems')
    def getAdditionalItems(self):
        """ Get all additional items on this plan. """
        pass


registerType(ExtropyPlan, PROJECTNAME)
