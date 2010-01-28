from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import BaseSchema, Schema, BaseFolder
from Products.Archetypes.public import ReferenceField, ReferenceWidget
from Products.Archetypes.public import LinesField, MultiSelectionWidget
from Products.Archetypes.public import registerType
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import StringField, StringWidget, DateTimeField, IntegerField, CalendarWidget, BooleanWidget, BooleanField, SelectionWidget,FileField,FileWidget, ImageField, ImageWidget, TextField, TextAreaWidget

from jarn.extranet.config import PROJECTNAME
from jarn.extranet.interfaces import IContract


ContractSchema = BaseSchema + Schema((

    StringField(name='contract_number'),

    StringField(name='contract_type',
                widget=SelectionWidget(label='Contract type'),
                vocabulary=DisplayList((('support','Support'),
                                        ('development','Development or consulting'),
                                        ('hosting','Hosting')
                                        )),                                      
                                       
                ),

    TextField('contract_terms',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Notable contract terms',
                                    description='This field is for internal use',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='',
                                    rows=5),
              ),


    FileField('orginial_contract',
              widget=FileWidget(label='Original Signed Contract', 
                                description="A scanned copy of the full contract text. Preferably the signed version")
        ),


    TextField('orginial_contract_text',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              searchable=True,
              widget=TextAreaWidget(label='The full contract text contents',
                                    description='The full contract text. Optional.',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='',
                                    rows=5),
              ),
    



            
    DateTimeField(name='startDate',
        accessor='start',
        widget=CalendarWidget(label='Start Date / Time',
                              label_msgid='label_startdate',
                              description='',
                              description_msgid='help_startdate',
                              ),
                  ),

    DateTimeField(name='endDate',
                  accessor='end',
                  widget=CalendarWidget(label='End Date / Time',
                                        label_msgid='label_end_date',
                                        description='',
                                        description_msgid='help_end_date',
                                        ),
                    ),
     
     
    # BILLING SCHEMA

    TextField('billing_address',
              schemata='billing',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Billing address',
                                    description='Billing address for invoices',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='',
                                    rows=5),
              ),


    StringField(name='currency',
                schemata='billing',
                default='NOK',
                widget=SelectionWidget(label='Currency'),
                                       vocabulary=DisplayList([('NOK','NOK'),('EUR','EUR'),('USD','USD')]),                                      
                ),

    StringField(name='charge_type',
                schemata='billing',
                widget=SelectionWidget(label='Charge type'),
                vocabulary=DisplayList([('timeandmaterials','Time and materials'),
                                        ('fixed','Fixed price')
                                       ]),                                      
                ),

    BooleanField('charge_mva',
                 schemata='billing',
                 widget=BooleanWidget(label='MVA/VAT',
                                      description='Check this if we should charge MVA/VAT',
                                      )
                 ),


    TextField('invoicing rules',
              schemata='billing',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Invoicing rules',
                                    description='How often can we invoice, under what terms?',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='',
                                    rows=5),
              ),

    IntegerField('cost_ceiling',
                 schemata='billing',
                 required = False,
                 default = None,
                 widget = StringWidget(label = 'Cost Ceiling', 
                                       description='Agreed max price for the contract',
                                       ),
                 ),

    StringField(name='recurring_invoicing_frequency',
                schemata='billing',
                widget=SelectionWidget(label='Invoicing frequency (for recurring invoices)'),
                vocabulary=DisplayList([('','Not Recurring'),
                                        ('monthly','Monthly'),
                                        ('quarterly','Quarterly'),
                                        ('every6','Every 6 months'),
                                        ('every12','Annually'),
                                       ]),                                      
                ),

    IntegerField('recurring_fee',
                schemata='billing',
                required = False,
                default = None,
                widget = StringWidget(label = 'Recurring fee', 
                                      description='Fee per period for recurring contracts',
                                       ),
                ),
                

    ))



class Contract(BaseFolder):
    """A contract for work"""
    schema = ContractSchema
    _at_rename_after_creation = True

    implements(IContract)


    security = ClassSecurityInfo()

registerType(Contract, PROJECTNAME)
