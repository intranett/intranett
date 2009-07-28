from types import StringTypes

from Acquisition import aq_base, aq_parent, aq_inner
from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.Archetypes.public import *
from Products.Archetypes.config import REFERENCE_CATALOG

from Products.CMFCore.utils import getToolByName

from Products.Extropy.config import *
from Products.Extropy.content.ExtropyBase import ExtropyBase, ExtropyBaseSchema, ParticipantsSchema, ChangeNoteSchema, TimeSchema, EstimatesSchema
from Products.Extropy.content.ExtropyHistoryTrackable import ExtropyHistoryTrackable

from Products.CMFCore import permissions

from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

from Products.Extropy.interfaces import IExtropyTask, z3IExtropyTask
from Products.Extropy.interfaces import IExtropyBase

from DateTime import DateTime


ExtropyTaskSchema = ExtropyBaseSchema.copy() + ParticipantsSchema.copy() + TimeSchema.copy() +  ChangeNoteSchema.copy() + EstimatesSchema.copy() + Schema((
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


    __implements__ = (IExtropyBase, IExtropyTask, INonStructuralFolder)
    implements(z3IExtropyTask)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.ModifyPortalContent, 'splitTask')
    def splitTask(self, targetPhase=None):
        """ make a new task with a reference pointing to this one"""
        rt = getToolByName(self, REFERENCE_CATALOG)
        if isinstance(targetPhase, StringTypes):
            targetPhase = rt.lookupObject(targetPhase)
        if targetPhase is None:
            targetPhase = aq_parent(aq_inner(self))

        newid = self.generateUniqueId(type_name='ExtropyTask')

        mungedid = targetPhase.invokeFactory(self.portal_type, newid)
        id = mungedid is not None and mungedid or newid
        newtask = getattr(targetPhase, id)
        # copy values
        #newtask.setKeywords(self.getRawKeywords())
        newtask.setResponsiblePerson(self.getRawResponsiblePerson())
        newtask.setParticipants(self.getRawParticipants())
        newtask.addReference(self, ORIGINATING_TASK_RELATIONSHIP)
        # we must also make sure to copy the pointer back to the feature
        if self.getOriginatingFeature():
            newtask.addReference(self.getOriginatingFeature(), TASK_FOR_RELATIONSHIP)
        newtask.reindexObject() # for featureUID
        return newtask

    security.declareProtected(VIEW_PERMISSION, 'getSplitTasks')
    def getSplitTasks(self):
        """Get the tasks split from this
        """
        return self.getBRefs(ORIGINATING_TASK_RELATIONSHIP)

    security.declareProtected(VIEW_PERMISSION, 'getOriginatingTask')
    def getOriginatingTask(self):
        """Get the originating task from which we were split
        """
        originating_task = self.getRefs(ORIGINATING_TASK_RELATIONSHIP)
        return originating_task and originating_task[0] or None

    def getOriginatingFeature(self):
        """Get the originating feature
        """
        return self.getExtropyParent(metatype='ExtropyFeature')

    def timeTillDue(self):
        """the amount of time left before the task is due to be delivered"""
        return self.getDueDate() - DateTime()

    # the accessor for estimated time is "getEstimatedDuration"

    def getWorkedHours(self):
        timetool = getToolByName(self,TIMETOOLNAME)
        hours = timetool.countIntervalHours(node=self)
        return hours

    security.declareProtected(VIEW_PERMISSION, 'getRemainingTime')
    def getRemainingTime(self):
        """ the remaining time till this task is complete, according to estimats"""
        #if the state is not one of the open ones > return 0
        tool = getToolByName(self,TOOLNAME)
        wftool = getToolByName(self,'portal_workflow')

        if not wftool.getInfoFor(self, 'review_state') in  tool.getOpenStates():
            return 0
        estimates = self.getEstimatedDuration()
        worked = self.getWorkedHours()
        if worked > estimates:
            return 0
        return estimates - worked

    ############################################
    # reindex parent on any change

    security.declareProtected(MODIFY_CONTENT_PERMISSION , 'indexObject')
    def indexObject(self):
        """"""
        #parent will reindex itself when we are added
        BaseFolder.indexObject(self)
        parent = aq_parent(aq_inner(self))
        if parent is not None:
            parent.reindexObject()

    security.declareProtected(MODIFY_CONTENT_PERMISSION , 'unindexObject')
    def unindexObject(self):
        """"""
        # reindex parent if we are removed
        BaseFolder.unindexObject(self)
        parent = aq_parent(aq_inner(self))
        if parent is not None:
            parent.reindexObject()

    security.declareProtected(MODIFY_CONTENT_PERMISSION , 'reindexObject')
    def reindexObject(self, idxs=[]):
        """"""
        # reindex parent if we are changed
        BaseFolder.reindexObject(self, idxs)
        parent = aq_parent(aq_inner(self))
        if parent is not None:
            parent.reindexObject()



registerType(ExtropyTask, PROJECTNAME)
