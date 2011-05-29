from zope.interface import implements

from DateTime import DateTime
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.permissions import ModifyPortalContent

from Products.Extropy.config import OPEN_STATES
from Products.Extropy.config import VIEW_PERMISSION
from Products.Extropy.config import DEFAULT_BUGDET_CATEGORIES
from Products.Extropy.interfaces import IExtropyBase

ExtropyBaseSchema = BaseSchema.copy() + Schema((

    TextField(
        name='text',
        required=False,
        searchable=True,
        primary=True,
        storage=AnnotationStorage(migrate=True),
        default_content_type='text/x-rst',
        default_output_type='text/x-html-safe',
        widget=RichWidget(
            label='Body Text',
            label_msgid='label_body_text',
            description='',
            description_msgid='help_body_text',
            rows=25,
            i18n_domain='plone',
        ),
    ),

    StringField(
        name='clientNotifyEmail',
        widget=StringWidget(
            label='Email for automatic reporting to the client',
            label_msgid='label_responsible_person',
            description='',
            description_msgid='help_responsible_person',
            i18n_domain='extropy',
        ),
    ),
))

ExtropyBaseSchema['description'].schemata = 'default'

TimeSchema = Schema((

    DateTimeField(
        name='startDate',
        accessor='start',
        default_method='getDefaultStart',
        widget=CalendarWidget(
            label='Start Date / Time',
            label_msgid='label_startdate',
            description='',
            description_msgid='help_startdate',
            i18n_domain='extropy',
        ),
    ),

    DateTimeField(
        name='endDate',
        accessor='end',
        default_method='getDefaultEnd',
        widget=CalendarWidget(
            label='End Date / Time',
            label_msgid='label_end_date',
            description='',
            description_msgid='help_end_date',
            i18n_domain='extropy',
        ),
    ),

))

ParticipantsSchema = Schema((

    LinesField(
        name='participants',
        vocabulary='getAvailableParticipants',
        multiValued=1,
        widget=MultiSelectionWidget(
            label='Participants',
            label_msgid='label_participants',
            description='',
            description_msgid='help_participants',
            i18n_domain='extropy',
        ),
    ),

    StringField(
        name='responsiblePerson',
        vocabulary='getAvailableParticipants',
        default_method='getDefaultResponsible',
        widget=SelectionWidget(
            label='Responsible Person',
            label_msgid='label_responsible_person',
            description='',
            description_msgid='help_responsible_person',
            i18n_domain='extropy',
        ),
    ),

))

BudgetSchema = Schema((
    StringField(
        name='budgetCategory',
        vocabulary=DEFAULT_BUGDET_CATEGORIES,
        default_method='getDefaultBudgetCategory',
        widget=SelectionWidget(
            label="Budget Category",
            label_msgid='',
            description="What is the main budget category? If you work on a "
                        "project and don't know what to put, use Billable.",
            description_msgid = "",
            i18n_domain='extropy',
        ),
    ),

))

ExtropyFullSchema = ExtropyBaseSchema + TimeSchema + ParticipantsSchema


class ExtropyBase:
    """Base class for shared Extropy stuff."""
    implements(IExtropyBase,)

    security = ClassSecurityInfo()

    security.declarePrivate('getExtropyParentChain')
    def getExtropyParentChain(self, include_self=False):
        """Gets the containg parent chain."""
        chain = []
        for o in self.aq_chain:
            if not include_self and o is self:
                continue
            if IExtropyBase.providedBy(o):
                chain.append(o)
        return chain

    def getExtropyProject(self):
        """Returns the current project."""
        if self.meta_type == 'ExtropyProject':
            return self
        return self.getExtropyParent(metatype='ExtropyProject')

    def getProjectTitle(self):
        """Returns the title of the current project."""
        p = self.getExtropyProject()
        return p and p.Title() or ''

    def getExtropyPhase(self):
        """Returns the current phase."""
        if self.meta_type == 'ExtropyPhase':
            return self
        return self.getExtropyParent(metatype='ExtropyPhase')

    def getPhaseTitle(self):
        """Returns the title of the current phase."""
        p = self.getExtropyPhase()
        return p and p.Title() or ''

    security.declarePrivate('getExtropyParent')
    def getExtropyParent(self, metatype=None):
        """Gets the containg parent, if it is an ExtropyBase object."""
        for o in self.aq_chain:
            if o is not self:
                if IExtropyBase.providedBy(o):
                    if metatype is None:
                        return o
                    elif hasattr(o,'meta_type') and metatype == o.meta_type:
                        return o
        return None

    security.declareProtected(ModifyPortalContent, 'setParticipants')
    def setParticipants(self, value, **kw):
        """Sets participants and update localroles.

        In the future we'll use TeamSpace.
        """
        oldparticipants = dict.fromkeys(self.getParticipants())
        newparticipants = dict.fromkeys(value)

        removed = [x for x in oldparticipants if not newparticipants.has_key(x)]

        if kw.has_key('schema'):
            schema = kw['schema']
        else:
            schema = self.Schema()
            kw['schema'] = schema
        res = schema['participants'].set(self, value, **kw)

        # Remove local roles
        for person in removed:
            oldroles = self.get_local_roles_for_userid(person)
            newroles = [role for role in oldroles if role not in ('Participant', 'Owner')]
            if newroles:
                self.manage_setLocalRoles(person, newroles)
            else:
                self.manage_delLocalRoles([person])

        return res

    security.declareProtected(VIEW_PERMISSION, 'getAvailableParticipants')
    def getAvailableParticipants(self):
        """Gets available participants from the containing project."""
        project = self.getExtropyProject()
        participants = project.getParticipants()
        return participants

    def getDefaultStart(self):
        """A reasonable default for start-time."""
        parent = self.getExtropyParent()
        if parent is not None:
            start = parent.start()
            return start and DateTime(start.Date())

    def getDefaultEnd(self):
        """A reasonable default for end-time."""
        parent = self.getExtropyParent()
        if parent is not None:
            end = parent.end()
            return end and DateTime(end.Date())

    def getDefaultResponsible(self, *args, **kwargs):
        if getattr(self, 'getProjectManager', None) is not None:
            return self.getProjectManager(*args, **kwargs)

    def setResponsiblePerson(self, value, **kw):
        """Sets the responsible person and makes sure wfstate is correct."""
        if kw.has_key('schema'):
            schema = kw['schema']
        else:
            schema = self.Schema()
            kw['schema'] = schema
        res = schema['responsiblePerson'].set(self, value, **kw)

        # Should also remove the person in question from the nosy list.
        # No need to be both places

        wftool = getToolByName(self, 'portal_workflow')
        try:
            state = wftool.getInfoFor(self, 'review_state')
            if value and state == 'unassigned':
                wftool.doActionFor(self, 'assign')
            elif not value:
                if state == 'assigned':
                    wftool.doActionFor(self, 'unassign')
                elif state == 'active':
                    wftool.doActionFor(self, 'deactivate')
                    wftool.doActionFor(self, 'unassign')
        except WorkflowException:
            pass
        return res

    security.declareProtected(VIEW_PERMISSION, 'getOpenWorkflowStates')
    def getOpenWorkflowStates(self):
        """The workflow states that are classified as open."""
        return OPEN_STATES

    security.declareProtected(VIEW_PERMISSION, 'getDefaultBudgetCategory')
    def getDefaultBudgetCategory(self):
        """The default budget category."""
        if hasattr(self.aq_parent, 'getBudgetCategory'):
            return self.aq_parent.getBudgetCategory() or 'Billable'
        return 'Billable'
