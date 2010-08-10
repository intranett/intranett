from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent
from Products.Archetypes.public import registerType
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import TextField
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.CMFCore.utils import getToolByName
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.Extropy.config import VIEW_PERMISSION
from Products.Extropy.config import TIMETOOLNAME

from jarn.extranet.config import PROJECTNAME
from jarn.extranet.interfaces import IContract


ContractSchema = ATFolderSchema + Schema((

    StringField(name='contract_number',
                widget=StringWidget(label='Contract number'),
                ),

    StringField(name='contract_type',
                widget=SelectionWidget(label='Contract type'),
                default='development',
                vocabulary=DisplayList((('support', 'Support'),
                                        ('development', 'Development or consulting'),
                                        ('hosting', 'Hosting'),
                                        )),

                ),

    StringField(
        name='projectManager',
        widget=StringWidget(
            label='Project Manager',
            size='20',
        ),
    ),

    StringField(
        name='projectStatus',
        widget=StringWidget(
            label='Project Status',
            description='The current project status.',
            size='60',
        ),
    ),

    DataGridField('work_types',
            columns=('description', 'rate'),
            default=({'description': 'Development', 'rate': '1200 NOK'}, ),
            widget = DataGridWidget(
                    label = 'Work types',
                    ),
            ),

    TextField('contract_terms',
              default_content_type='text/plain',
              allowable_content_types=('text/plain', ),
              widget=TextAreaWidget(label='Notable contract terms',
                                    description='This field is for internal use',
                                    rows=5),
              ),


    FileField('original_contract',
              widget=FileWidget(label='Original Signed Contract',
                                description="A scanned copy of the full contract text. Preferably the signed version")
        ),


    TextField('original_contract_text',
              default_content_type='text/plain',
              allowable_content_types=('text/plain', ),
              searchable=True,
              widget=TextAreaWidget(label='The full contract text contents',
                                    description='The full contract text. Optional.',
                                    rows=5),
              ),

    DateTimeField(name='startDate',
        accessor='start',
        widget=CalendarWidget(label='Start Date / Time')
        ),

    DateTimeField(name='endDate',
                  accessor='end',
                  widget=CalendarWidget(label='End Date / Time'),
                  ),

    TextField('invoicing_rules',
              default_content_type='text/plain',
              allowable_content_types=('text/plain', ),
              widget=TextAreaWidget(label='Invoicing rules',
                                    description='How often can we invoice, under what terms?',
                                    rows=5),
              ),

    ))


class Contract(ATFolder):
    """A contract for work"""

    _at_rename_after_creation = True
    implements(IContract)

    schema = ContractSchema
    security = ClassSecurityInfo()

    security.declareProtected(VIEW_PERMISSION, 'getUniqueWork_types')
    def getUniqueWork_types(self):
        """"""
        # value = ({'rate': '1200 NOK', 'description': 'development'}, )
        values = self.getField('work_types').get(self)
        types = []
        for row in values:
            types.append(row['description'])
        return types

    security.declareProtected(VIEW_PERMISSION, 'getActivePhases')
    def getActivePhases(self):
        """"""
        return ()

    security.declareProtected(VIEW_PERMISSION, 'getActivities')
    def getActivities(self, **kw):
        """"""
        return ()

    security.declareProtected(VIEW_PERMISSION, 'getExtropyProject')
    def getExtropyProject(self):
        """Returns the current project."""
        return self

    security.declarePrivate('getExtropyParentChain')
    def getExtropyParentChain(self, include_self=False):
        """Gets the containg parent chain."""
        if include_self:
            return [self]
        return []

    security.declarePrivate('getResponsiblePerson')
    def getResponsiblePerson(self):
        """fake responsible person for indexing"""
        return ['all']

    security.declareProtected(VIEW_PERMISSION, 'getProjectTitle')
    def getProjectTitle(self):
        """Returns the title of the current project."""
        return aq_parent(self).Title()

    security.declareProtected(VIEW_PERMISSION, 'getWorkedHours')
    def getWorkedHours(self):
        """get the total amount of time worked for this object"""
        tool = getToolByName(self,TIMETOOLNAME)
        return tool.countIntervalHours(node=self)

    security.declareProtected(VIEW_PERMISSION, 'getUnbilledTime')
    def getUnbilledTime(self):
        """get the amount of unilled time worked for this object"""
        tool = getToolByName(self, TIMETOOLNAME)
        return tool.countIntervalHours(node=self,
            review_state='entered', getBudgetCategory='Billable')

    security.declareProtected(VIEW_PERMISSION, 'getBudgetCategory')
    def getBudgetCategory(self):
        """The budget category."""
        return 'Billable'

    security.declareProtected(VIEW_PERMISSION, 'getDefaultBudgetCategory')
    def getDefaultBudgetCategory(self):
        """The default budget category."""
        return 'Billable'

registerType(Contract, PROJECTNAME)
