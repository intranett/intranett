from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import registerType
from Products.Archetypes.public import BaseFolder
from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import FileField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import TextField

from jarn.extranet.config import PROJECTNAME
from jarn.extranet.interfaces import IContract


ContractSchema = BaseSchema + Schema((

    StringField(name='contract_number'),

    StringField(name='contract_type',
                widget=SelectionWidget(label='Contract type'),
                vocabulary=DisplayList((('support', 'Support'),
                                        ('development', 'Development or consulting'),
                                        ('hosting', 'Hosting'),
                                        )),

                ),

    TextField('contract_terms',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Notable contract terms',
                                    description='This field is for internal use',
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


    # BILLING SCHEMA

    TextField('billing_address',
              schemata='billing',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Billing address',
                                    description='Billing address for invoices',
                                    rows=5),
              ),


    StringField(name='currency',
                schemata='billing',
                default='NOK',
                widget=SelectionWidget(label='Currency'),
                                       vocabulary=DisplayList([('NOK', 'NOK'), ('EUR', 'EUR'), ('USD', 'USD')]),
                ),

    StringField(name='charge_type',
                schemata='billing',
                widget=SelectionWidget(label='Charge type'),
                vocabulary=DisplayList([('timeandmaterials', 'Time and materials'),
                                        ('fixed', 'Fixed price'),
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
                vocabulary=DisplayList([('', 'Not Recurring'),
                                        ('monthly', 'Monthly'),
                                        ('quarterly', 'Quarterly'),
                                        ('every6', 'Every 6 months'),
                                        ('every12', 'Annually'),
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

    _at_rename_after_creation = True
    implements(IContract)

    schema = ContractSchema
    security = ClassSecurityInfo()


registerType(Contract, PROJECTNAME)
