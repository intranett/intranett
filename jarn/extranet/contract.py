from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import BaseSchema, Schema, BaseFolder
from Products.Archetypes.public import ReferenceField, ReferenceWidget
from Products.Archetypes.public import LinesField, MultiSelectionWidget
from Products.Archetypes.public import registerType
from Products.Archetypes.public import DisplayList

from jarn.extranet.config import PROJECTNAME

ContractSchema = BaseSchema + Schema((

    StringField(name='contract_number'),

    StringField(name='contract_type',
                widget=SelectionWidget(label='Contract type'),
                vocabulary=DisplayList([('support','Support'),
                                        ('development','Development or consulting')
                                        ('hosting','Hosting')
                                        ]),                                      
                                       
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
     

    TextField('invoicing rules',
              schemata='billing',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Invoicing rules',
                                    description='How often can we invoice, under whart terms?',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='',
                                    rows=5),
              ),

    BooleanField('charge_mva',
                 schemata='billing',
                 widget=BooleanWidget(label='Charge MVA/VAT')
                 ),


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

    IntegerField('cost_ceiling',
                 schemata='billing',
                 required = True,
                 default = None,
                 widget = StringWidget(label = 'Cust Ceiling', 
                                       description='Maximum price for the contract',
                                       ),
                 ),

    StringField(name='charge_type',
                schemata='billing',
                widget=SelectionWidget(label='Charge type'),
                vocabulary=DisplayList([('timeandmaterials','Time and materials'),
                                        ('fixed','Fixed price')
                                       ]),                                      
                ),

    IntegerField('recurring_fee',
                schemata='billing',
                required = True,
                default = None,
                widget = StringWidget(label = 'Cust Ceiling', 
                                      description='Maximum price for the contract',
                                       ),
                ),


    StringField(name='recurring_invoicing_frequency',
                schemata='billing',
                widget=SelectionWidget(label='Invoicing frequency (for recurring invoices)'),
                vocabulary=DisplayList([('monthly','Monthly'),
                                        ('quarterly','Quarterly'),
                                        ('every6','Every 6 months'),
                                        ('every12','Annually'),
                                       ]),                                      
                ),



    StringField(name='currency',
                schemata='billing',
                widget=SelectionWidget(label='Currency'),
                vocabulary=DisplayList(['EUR','NOK','USD']),                                      
                )

    ))



class Contract(BaseFolder):
    """A contract for work"""
    schema = ContractSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

registerType(Contract, PROJECTNAME)
