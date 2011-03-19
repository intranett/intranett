from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Extropy.config import *
from Products.Extropy.content.ExtropyBase import ExtropyBase
from Products.Extropy.content.ExtropyHistoryTrackable import ExtropyHistoryTrackable
from Products.Extropy.content.ExtropyBase import ExtropyBaseSchema, ChangeNoteSchema
from Products.Extropy.interfaces import IExtropyBug
from Products.CMFPlone.interfaces import INonStructuralFolder


BugSchema = ExtropyBaseSchema.copy() + ChangeNoteSchema.copy()

class ExtropyBug(ExtropyHistoryTrackable, ExtropyBase, BaseFolder):
    """A bug is a reported defect in the work produced."""

    schema = BugSchema

    meta_type = portal_type = 'ExtropyBug'
    archetype_name = 'Bug'
    content_icon = 'bug_icon.gif'

    filter_content_types = 1
    allowed_content_types = ('ExtropyTaskHistory',)
    global_allow = 0
    allow_discussion = 0

    security = ClassSecurityInfo()
    implements(IExtropyBug, INonStructuralFolder)


    def spawnTask(self, container=None):
        """ create a linked task from this bug. """
        # If Container is None, put the task some convenient place, like the active phase
        pass

    def getSpawnedTasks(self):
        """ return all linked tasks"""
        pass

    def getOpenSpawnedTasks(self):
        """Only the open ones"""
        pass

registerType(ExtropyBug, PROJECTNAME)
