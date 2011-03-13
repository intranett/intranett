from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *

from Products.CMFCore.utils import getToolByName

from Products.Extropy.config import *
from Products.Extropy.content.ExtropyBase import ExtropyBase, ExtropyBaseSchema, ParticipantsSchema, ChangeNoteSchema, TimeSchema
from Products.Extropy.content.ExtropyHistoryTrackable import ExtropyHistoryTrackable

from Products.CMFPlone.interfaces import INonStructuralFolder

from Products.Extropy.interfaces import IExtropyTask
from Products.Extropy.interfaces import IExtropyBase

from DateTime import DateTime


ExtropyTaskSchema = ExtropyBaseSchema.copy() + ParticipantsSchema.copy() + TimeSchema.copy() +  ChangeNoteSchema.copy() + Schema((
    StringField('priority',
        vocabulary = TASK_PRIORITIES,
        default=5,
        widget = SelectionWidget(
            label = "Priority",
            description = "Task Priority",
            label_msgid = "label_priority",
            description_msgid = "help_priority",
    )),

))

class ExtropyTask(ExtropyHistoryTrackable, ExtropyBase, BaseFolder):
    """A task is a clearly defined unit of work that can be completed."""

    schema = ExtropyTaskSchema


    implements(IExtropyBase, IExtropyTask, INonStructuralFolder)

    security = ClassSecurityInfo()

    def getOriginatingFeature(self):
        """Get the originating feature
        """
        return self.getExtropyParent(metatype='ExtropyFeature')

    def timeTillDue(self):
        """the amount of time left before the task is due to be delivered"""
        return self.getDueDate() - DateTime()

    def getWorkedHours(self):
        timetool = getToolByName(self,TIMETOOLNAME)
        hours = timetool.countIntervalHours(node=self)
        return hours


registerType(ExtropyTask, PROJECTNAME)
