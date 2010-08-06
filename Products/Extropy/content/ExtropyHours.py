from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Extropy.config import *
from Products.Extropy.permissions import *
from Products.Extropy.content.ExtropyBase import BudgetSchema
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.ATContentTypes.configuration import zconf


from Products.Extropy.interfaces import IExtropyBase

ExtropyHoursSchema = BaseSchema.copy() + Schema((

    StringField('id',
               widget=IdWidget(visible={ 'edit' :'hidden', 'view' : 'hidden' })
                ),

    DateTimeField('startDate',
                  accessor='start',
                  default_method='setDefaultStartDate' ,
                  widget = CalendarWidget(description="Enter the starting date and time, or click the calendar icon and select it. ",
                                          label="Work started",)
                  ),
    DateTimeField('endDate',
                  accessor='end',
                  default_method='setDefaultEndDate',
                  widget = CalendarWidget(description= "Enter the ending date and time, or click the calendar icon and select it. ",
                                          label = "Work ended",)
                  ),

    TextField('summary',
              required=False,
              searchable=True,
              primary=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              #validators = ('isTidyHtml',),
              default_content_type = zconf.ATDocument.default_content_type,
              default_output_type = 'text/x-html-safe',
              allowable_content_types = zconf.ATDocument.allowed_content_types,
              widget = RichWidget(
                        description = "",
                        description_msgid = "help_summary",
                        label = "Work summary",
                        label_msgid = "label_summary",
                        rows = 15,
                        i18n_domain = "plone",
                        allow_file_upload = zconf.ATDocument.allow_document_upload),
    ),

    StringField('worktype',
                  accessor='hourWorktype',
                  vocabulary=WORKTYPES,
                  widget=SelectionWidget(label='Work Type',),
                  ),

    StringField(
        name='invoiceNumber',
        widget=StringWidget(
            label='Invoice number',
            description='The invoice number this hour is billed on.',
            i18n_domain='extropy',
        ),
    ),

    )) + BudgetSchema.copy()


class ExtropyHours(BaseContent):
    """Hours track worked time. Each hour object represents a chunk of worked time."""

    schema         = ExtropyHoursSchema
    security       = ClassSecurityInfo()

    security.declarePrivate('getExtropyParent')
    def getExtropyParent(self, metatype=None):
        """Gets the containg parent, if it is an ExtropyBase object.
        """
        project_types=['ExtropyProject', 'Contract']
        for o in self.aq_chain:
            if o is not self:
                if hasattr(o,'meta_type') and o.meta_type in project_types:
                    return o
        return None

    security.declarePrivate('findBudgetCategory')
    def findBudgetCategory(self):
        p = self.getExtropyParent()
        if hasattr(p, 'budgetCategory'):
            return p.getBudgetCategory()
        return '-'

    def workedHours(self):
        """ the interval worked, in hours"""
        if self.end() is None or self.start() is None: return 0
        interval = self.end() - self.start()
        iHours = round(interval * 24.0 , 1)
        return iHours

    security.declarePublic('setDefaultStartDate')
    def setDefaultStartDate(self):
        """use smarts to find a proper default start-time"""
        start = getattr(self, 'startDate', None)
        if start is not None:
            return start
        ct = getToolByName(self, TIMETOOLNAME)
        lastreg =  ct.getLastRegisteredTime()
        if lastreg is not None:
            return lastreg
        else:
            return DateTime() - (1.0/24.0)

    security.declarePublic('setDefaultEndDate')
    def setDefaultEndDate(self):
        """one hour more"""
        return self.setDefaultStartDate() + (1.0/24.0)

    def getDate(self):
        if self.start() is None:
            return None
        return self.start().earliestTime()

    security.declarePublic('getDefaultBudgetCategory')
    def getDefaultBudgetCategory(self):
        """the default budget cat"""
        package =  self.getExtropyParent(metatype='ExtropyPhase')
        if package is not None:
            return package.getBudgetCategory() or 'Billable'
        return "Billable"

    # security.declareProtected(ModifyPortalContent, 'setStartDate')
    # def setStartDate(self, value, **kwargs):
    #     field = self.getField('startDate')
    #     field.set(self, value, **kwargs)
    #     parent = self.getExtropyParent()
    #     if parent is not None:
    #         parent.reindexObject()
    # 
    # security.declareProtected(ModifyPortalContent, 'setEndDate')
    # def setEndDate(self, value, **kwargs):
    #     field = self.getField('endDate')
    #     field.set(self, value, **kwargs)
    #     parent = self.getExtropyParent()
    #     if parent is not None:
    #         parent.reindexObject()


registerType(ExtropyHours, PROJECTNAME)
