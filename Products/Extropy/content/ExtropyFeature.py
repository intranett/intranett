import transaction
from Acquisition import aq_parent, aq_inner
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.Archetypes.public import registerType
from Products.Archetypes.public import Schema, BaseFolder
from Products.Archetypes.public import SelectionWidget, StringField
from Products.Extropy.content.ExtropyBase import TimeSchema
from Products.Extropy.content.ExtropyBase import ExtropyBase
from Products.Extropy.content.ExtropyBase import ExtropyBaseSchema
from Products.Extropy.content.ExtropyBase import ParticipantsSchema
from Products.Extropy.content.ExtropyTracking import ExtropyTracking
from Products.Extropy.content.ExtropyHistoryTrackable import ExtropyHistoryTrackable
from Products.Extropy.interfaces import IExtropyBase
from Products.Extropy.interfaces import IExtropyTracking
from Products.Extropy.interfaces import IExtropyFeature
from Products.Extropy import config

FeatureSchema = ExtropyBaseSchema.copy() + TimeSchema.copy() + ParticipantsSchema.copy() + Schema((

    StringField(
        name='moveToPhase',
        required=False,
        searchable=False,
        vocabulary='listProjectPhases',
        mutator='moveTo',
        widget=SelectionWidget(
            label='Move to',
            description='Move to phase',
            label_msgid='label_moveto',
            description_msgid='help_moveto',
            visible={'edit':'invisible', 'view': 'invisible'},
        ),
    ),

))


class ExtropyFeature(ExtropyHistoryTrackable, ExtropyTracking, ExtropyBase, BaseFolder):
    """A Deliverable is a clearly defined unit that should be produced as part of a project. Deliverables contain tasks."""
    __implements__ = BaseFolder.__implements__ + (IExtropyBase, IExtropyTracking, IExtropyFeature)

    schema = FeatureSchema
    security = ClassSecurityInfo()

    _at_rename_after_creation = True

    def getTargetPhase(self):
        """Calculates the target phase."""
        return self.getExtropyParent('ExtropyPhase')

    security.declareProtected(ModifyPortalContent, 'moveTo')
    def moveTo(self, uid):
        """Moves this object somewhere."""
        if not uid:
            return False
        parent = aq_parent(aq_inner(self))
        if parent is not None and uid != parent.UID():
            self._v_cp_refs = 1 # See Referenceable, keep refs on
                                # what is a move/rename
            rt = getToolByName(self, REFERENCE_CATALOG)
            dest = rt.lookupObject(uid)
            if dest is None:
                raise AttributeError, "we are trying to move to a None-object from uid %s" %(uid)
            dest.manage_pasteObjects(parent.manage_cutObjects(self.getId()))
            if hasattr(self, 'aq_parent'):
                self.aq_parent = dest
                # This is required to make sure the new aq_parent is used later on by scripts...
                self = aq_inner(self)
            transaction.get().savepoint()
            return self

    def getWorkedHours(self):
        """Gets the total amount of time worked for this object."""
        tool = getToolByName(self, config.TIMETOOLNAME)
        return tool.countIntervalHours(node=self)


registerType(ExtropyFeature, config.PROJECTNAME)
