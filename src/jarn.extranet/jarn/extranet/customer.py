from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import registerType
from Products.Archetypes.public import ImageField
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import TextField
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema

from jarn.extranet.config import PROJECTNAME
from jarn.extranet.interfaces import ICustomer


CustomerSchema = ATFolderSchema + Schema((

    StringField('code',
                required=True,
                widget=StringWidget(label='Unique customer code',
                                    description='Technical identifer used as the unique id in all tools.'),
                ),

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
              default_content_type='text/x-web-intelligent',
              allowable_content_types=('text/x-web-intelligent', ),
              default_output_type='text/x-html-safe',
              widget=TextAreaWidget(label='Billing address',
                                    description='Billing address for invoices',
                                    rows=5),
              ),

    TextField('billing_information',
              default_content_type='text/x-web-intelligent',
              allowable_content_types=('text/x-web-intelligent', ),
              default_output_type='text/x-html-safe',
              widget=TextAreaWidget(label='Internal billing information',
                                    description='Billing info for invoices. Not sent to customers',
                                    rows=5),
              ),

    ))


class Customer(ATFolder):
    """A archetype representative for a Jarn Customer"""

    _at_rename_after_creation = True
    schema = CustomerSchema
    security = ClassSecurityInfo()

    implements(ICustomer)


registerType(Customer, PROJECTNAME)
