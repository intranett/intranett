from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.CMFCore.utils import getToolByName
from Products.Extropy.content.ExtropyBase import ExtropyBase
from Products.Extropy.content.ExtropyBase import ExtropyBaseSchema, ParticipantsSchema
from Products.Extropy.content.ExtropyTracking import ExtropyTracking
from Products.Extropy.config import *
from Products.Extropy.interfaces import *

ActivitySchema = ExtropyBaseSchema.copy()+ ParticipantsSchema.copy() + Schema((
    ))

del ActivitySchema['responsiblePerson']

class ExtropyActivity(ExtropyTracking, ExtropyBase, BaseFolder ):
    """Activity is ongoing work that needs hour-registration"""
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
