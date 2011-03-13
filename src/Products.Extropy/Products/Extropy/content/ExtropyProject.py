from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *

from Products.CMFCore.utils import getToolByName

from Products.Extropy.config import *
from Products.Extropy.interfaces import IExtropyBase
from Products.Extropy.interfaces import IExtropyTracking
from Products.Extropy.content.ExtropyBase import TimeSchema
from Products.Extropy.content.ExtropyBase import BudgetSchema
from Products.Extropy.content.ExtropyBase import ExtropyBase
from Products.Extropy.content.ExtropyBase import ExtropyBaseSchema
from Products.Extropy.content.ExtropyTracking import ExtropyTracking
from Products.CMFPlone.utils import _createObjectByType


ExtropyProjectSchema = ExtropyBaseSchema.copy() + Schema((

    LinesField(
        name='participants',
        vocabulary='getAvailableParticipants',
        multiValued=1,
        widget=InAndOutWidget(
            label='Participants',
            description='',
            label_msgid='label_participants',
            description_msgid='help_participants',
            i18n_domain='extropy',
        ),
    ),

    StringField(
        name='projectManager',
        vocabulary='getAvailableParticipants',
        widget=SelectionWidget(
            label='Project Manager',
            description='The project manager get a copy of all mail generated in the project.',
            label_msgid='label_project_manager',
            description_msgid='help_project_manager',
            i18n_domain='extropy',
        ),
    ),

    StringField(
        name='technicalResponsible',
        vocabulary='getAvailableParticipants',
        widget=SelectionWidget(
            label='Technical Responsible',
            description='The technical responsible is the project lead coder.',
            label_msgid='label_technical_responsible',
            description_msgid='help_technical_responsible',
            i18n_domain='extropy',
        ),
    ),

    StringField(
        name='UIResponsible',
        vocabulary='getAvailableParticipants',
        widget=SelectionWidget(
            label='UI Responsible',
            description='The person responsible for all user interface work in the project.',
            label_msgid='label_ui_responsible',
            description_msgid='help_ui_responsible',
            i18n_domain='extropy',
        ),
    ),

    StringField(
        name='projectStatus',
        widget=StringWidget(
            label='Project Status',
            description='The current projetct status.',
            label_msgid='label_project_status',
            description_msgid='help_project_status',
            i18n_domain='extropy',
            size='60',
        ),
    ),

    LinesField(
         name='project_keywords',
         schemata='configuration',
    ),

    StringField(
        name='project_email_address',
        schemata='configuration',
    ),

)) +  TimeSchema.copy() + BudgetSchema.copy()


class ExtropyProject(ExtropyTracking, ExtropyBase, OrderedBaseFolder):
    """An Extropy Project contains all the information needed to manage a project."""
    implements(IExtropyTracking, IExtropyBase)

    schema = ExtropyProjectSchema

    security = ClassSecurityInfo()
    _at_rename_after_creation = True

    security.declareProtected('View','generateUniqueId')
    def generateUniqueId(self, type_name=None):
        """Override the unique-id generator to get cool sequential id-numbering"""
        typeswithnumbers = ['ExtropyTask','ExtropyBug']
        if not type_name in typeswithnumbers:
            return self.aq_parent.generateUniqueId(type_name=type_name)
        if not hasattr(self,'id_counter'):
            self.id_counter = 1
        newid = self.id_counter
        self.id_counter = newid + 1
        return str(newid)

    security.declareProtected('View','getPhases')
    def getPhases(self):
        """Gets the list of phases."""
        return self.objectValues(['ExtropyPhase'])

    security.declareProtected('View','getActivePhases')
    def getActivePhases(self):
        """Gets the active phases. we can have more than one."""
        extropytool = getToolByName(self, TOOLNAME)
        res = extropytool.localQuery(node=self, portal_type='ExtropyPhase', review_state='active')
        return [i.getObject() for i in res]

    security.declareProtected('View','getAvailableParticipants')
    def getAvailableParticipants(self):
        """Lists the users."""
        membertool   = getToolByName(self, 'portal_membership')
        user_list    = membertool.listMemberIds()
        return user_list

    def listContents(self):
        """Lists subobjects."""
        catalog = getToolByName(self, 'portal_catalog')
        results = catalog.searchResults(
            path = {'query' :'/'.join(self.getPhysicalPath()),
                    'depth' : 1,},
            sort_on = 'getObjPositionInParent',
            )
        return results


registerType(ExtropyProject, PROJECTNAME)
