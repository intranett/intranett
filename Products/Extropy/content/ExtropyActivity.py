from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Archetypes.config import REFERENCE_CATALOG
from math import floor
from Acquisition import aq_base, aq_parent, aq_inner
from types import StringTypes
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_parent
from Products.Extropy.content.ExtropyBase import ExtropyBase
from Products.Extropy.content.ExtropyBase import ExtropyBase, ExtropyBaseSchema, ParticipantsSchema, ChangeNoteSchema
from Products.Extropy.content.ExtropyTracking import ExtropyTracking
from Products.Extropy.config import *
from Products.Extropy.interfaces import *
from Products.CMFCore import permissions

ActivitySchema = ExtropyBaseSchema.copy()+ ParticipantsSchema.copy() + Schema((
    ))

del ActivitySchema['responsiblePerson']

class ExtropyActivity(ExtropyTracking, ExtropyBase, BaseFolder ):
    """Activity is ongoing work that needs hour-registration, but doesn't really have tasks as such. Generally speaking, they are deliverables that are never marked as being completed. Typically on-site work, training, administration, meetings."""
    implements(IExtropyBase, IExtropyTracking)

    schema = ActivitySchema

    security = ClassSecurityInfo()

    _at_rename_after_creation = True

    def getWorkedHours(self):
        """get the total amount of time worked for this object"""
        tool = getToolByName(self,TIMETOOLNAME)
        return tool.countIntervalHours(node=self)

    def getResponsiblePerson(self):
        """fake responsible person for indexing"""
        return self.getParticipants()


registerType(ExtropyActivity, PROJECTNAME)
