from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Products.Extropy.config import *
from Products.Extropy.interfaces import IExtropyBase
from Products.Extropy.interfaces import IExtropyTracking
from Products.Extropy.content.ExtropyBase import ExtropyBase
from Products.Extropy.content.ExtropyBase import TimeSchema,ExtropyBaseSchema,  BudgetSchema
from Products.Extropy.content.ExtropyTracking import ExtropyTracking


ExtropyPhaseSchema = ExtropyBaseSchema.copy() + TimeSchema.copy() + BudgetSchema.copy()


class ExtropyPhase(ExtropyTracking, ExtropyBase, BaseFolder):
    """A Package is a unit of work that contains a number of tasks. Aka. milestone in other systems."""
    implements(IExtropyTracking, IExtropyBase)

    schema = ExtropyPhaseSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    def getParticipants(self):
        """Gets the participants.
        """
        parent = self.getExtropyParent()
        if parent is not None:
            return parent.getParticipants()
        return []


registerType(ExtropyPhase, PROJECTNAME)
