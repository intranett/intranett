from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import registerType
from Products.Archetypes.public import BaseFolder
from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import ImageField
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import TextField

from jarn.extranet.config import PROJECTNAME
from jarn.extranet.interfaces import ICustomer


CustomerSchema = BaseSchema + Schema((

    TextField('description',
              accessor='Description',
              widget=TextAreaWidget(label='Description',
                                    description='',
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
                                    rows=5),
              ),

    TextField('billing_information',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Internal billing information',
                                    description='Billing info for invoices. Not sent to customers',
                                    rows=5),
              ),

    ))


class Customer(BaseFolder):
    """A archetype representative for a Jarn Customer"""

    _at_rename_after_creation = True
    schema = CustomerSchema
    security = ClassSecurityInfo()

    implements(ICustomer)


registerType(Customer, PROJECTNAME)
