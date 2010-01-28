from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import BaseSchema, Schema, BaseFolder
from Products.Archetypes.public import ReferenceField, ReferenceWidget
from Products.Archetypes.public import LinesField, MultiSelectionWidget
from Products.Archetypes.public import registerType
from Products.Archetypes.public import DisplayList

from Products.Archetypes.public import StringField, ImageField, ImageWidget, TextField, TextAreaWidget


from jarn.extranet.config import PROJECTNAME
from jarn.extranet.interfaces import ICustomer, IPerson

CustomerSchema = BaseSchema + Schema((

    TextField('description',
              accessor='Description',
              widget=TextAreaWidget(label='Description',
                                    description='',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='',
                                    rows=5),
              ),

    
    ImageField('logo',
        widget=ImageWidget(label='Customer logo')
        ),
    
    TextField('billing_address',
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

    TextField('billing_information',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Internal billing information',
                                    description='Billing info for invoices. Not sent to customers',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='',
                                    rows=5),
              ),



    ))



class Customer(BaseFolder):
    """A archetype representative for a Jarn Customer"""
    schema = CustomerSchema
    _at_rename_after_creation = True

    implements(ICustomer)

    security = ClassSecurityInfo()


registerType(Customer, PROJECTNAME)
