from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *

from Products.Invoice.config import *
from Products.Invoice import permissions
from Products.Invoice.interfaces import IInvoice

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr



from Products.DataGridField import DataGridField, DataGridWidget

from DateTime import DateTime

InvoiceSchema = BaseSchema.copy() + Schema((

    ComputedField(name='title',
        searchable=True,
        accessor='Title',
        expression='(str("#" + str(context.getInvoiceNumber()) + " " +context.getToName())).strip()',
        widget=ComputedWidget(
            visible = {'view': 'invisible', 'edit': 'invisible'},
        ),
    ),

    IntegerField('invoiceNumber',
              required = True,
              searchable = True,
              default = None,
              index = "FieldIndex:schema",
              widget = StringWidget(label = 'Invoice Number'),
              default_method = 'getDefaultInvoiceNumber'
            ),


    StringField('Header',
              searchable = True,
              required = False,
              default= '',
              widget = StringWidget(label = 'Header'),
            ),


    StringField('fromName',
              required = True,
              searchable = False,
              default = DEFAULT_FROM_COMPANY,
              widget = StringWidget(
                    label = 'From'
                    )
            ),

    TextField('fromAddress',
              searchable = False,
              default_content_type = 'text/x-rst',
              default_output_type = 'text/x-html-safe',
              default = DEFAULT_FROM_COMPANY_ADRESS,
              widget = TextAreaWidget(
                    label = 'From address'
                    )
            ),

    StringField('vatNumber',
              required = False,
              searchable = False,
              default = DEFAULT_VAT_NUMBER,
              widget = StringWidget(label = 'VAT/Organisation Number'),
            ),


    StringField('toName',
              searchable = True,
              required = True,
              widget = StringWidget(label = 'To'),
            ),

    TextField('toAddress',
              searchable = False,
              default_content_type = 'text/x-rst',
              default_output_type = 'text/x-html-safe',
              widget = TextAreaWidget(
                    label = 'To address'
                    )
            ),

    DateTimeField('invoiceDate',
              required = True,
              searchable = True,
              default_method = 'today',
              widget = CalendarWidget(show_hm = False, label = 'Invoice Date'),
            ),


    StringField('Currency',
              searchable = True,
              required = True,
              default= 'EUR',
            ),

    DataGridField('invoiceLines',
            columns=('description', 'amount'),
            default=({'description':'', 'amount':''},),
            widget = DataGridWidget(
                    label = 'Invoice Lines',
                    ),
            ),

    ComputedField('total',
              searchable = False,
              expression = 'context.calculatetotal()'
            ),

    IntegerField('paymentDays',
              required = True,
              searchable = False,
              default = 21,
              vocabulary = PAYMENT_DUE_OPTIONS,
              widget = SelectionWidget(label = 'Payment Due In')
              ),

    TextField('paymentDetails',
              required = False,
              searchable = False,
              default_content_type = 'text/x-rst',
              default_output_type = 'text/x-html-safe',
              default = DEFAULT_PAYMENT_DETAILS,
              widget = TextAreaWidget(
                    label = 'Payment Details',
                    description="Account numbers and other relevant payment information."
                    )
            ),

    TextField('notes',
              required = False,
              searchable = False,
              default_content_type = 'text/x-rst',
              default_output_type = 'text/x-html-safe',
              default = DEFAULT_NOTE_TEXT,
              widget = TextAreaWidget(
                    label = 'Notes'
                    )
            )
))


InvoiceSchema['description'].schemata='default'
InvoiceSchema['description'].default=''


class Invoice(BaseContent):
    """Invoice content type.
    """
    implements(IInvoice)

    schema = InvoiceSchema
    meta_type = portal_type = archetype_name = 'Invoice'
    security = ClassSecurityInfo()
    content_icon = 'invoice_icon.gif'

    _at_rename_after_creation = True


    actions = ({
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${object_url}/invoice_view',
        'permissions' : ('View',),
         }, {
        'id'          : 'edit',
        'name'        : 'Edit',
        'action'      : 'string:${object_url}/base_edit',
        'permissions' : (permissions.EDIT_CONTENT_PERMISSION,),
         },)


    security.declareProtected('View', 'today')
    def today(self):
        """Assign today
        """
        return DateTime()

    _v_default = None
    security.declareProtected('View', 'getDefaultInvoiceNumber')
    def getDefaultInvoiceNumber(self):
        """Query catalog for the higest numbered/last invoice and add 1 """
        # getDefaultInvoiceNumber can/will be called more than once. Cache the 
        # result the first time.
        if self._v_default is None:
            pc = self.portal_catalog
            invoices = pc.searchResults(Type='Invoice',
                                        sort_on='getInvoiceNumber', 
                                        sort_order='desc')
            if len(invoices) == 0:
                self._v_default = 1
            else:
                self._v_default = invoices[-1].getInvoiceNumber + 1
        return self._v_default

    security.declareProtected('View', 'getPaymentdue')
    def getPaymentdue(self):
        """Convert payment due to absolute date"""
        return self.getInvoiceDate() + self.getPaymentDays()

    security.declareProtected('View', 'calculatetotal')
    def calculatetotal(self):
        """Calculate the invoice total amount
        """
        invcollist = self.schema['invoiceLines'].getColumn(self, 'amount')
        totalamount = 0.
        for amount_item in invcollist:
            try:
                totalamount = totalamount + float(amount_item)
                totalamount = int(totalamount)
            except ValueError:
                totalamount = "*ERROR*"
                break
        return totalamount

    security.declareProtected('View', 'end')
    def end(self):
        """catalog index for portlets"""
        return self.getPaymentdue()

    def generateNewId(self):
        """Suggest an id for this object.
        This id is used when automatically renaming an object after creation.
        """
        plone_tool = getToolByName(self, 'plone_utils', None)
        if plone_tool is None or not shasattr(plone_tool, 'normalizeString'):
            return None

        title = 'invoice-' + str(self.getInvoiceNumber()).zfill(5)
        return plone_tool.normalizeString(title)


    security.declareProtected(permissions.EDIT_CONTENT_PERMISSION, 'createRecurrence')
    def createRecurrence(self):
        """take the current invoice, and make a new recurrence of it"""
        parent = self.aq_parent
        parent.manage_pasteObjects(parent.manage_copyObjects(self.getId()))
        newob = parent['copy_of_'+self.getId()]
        newob.setInvoiceNumber(newob.getDefaultInvoiceNumber())
        newob.setInvoiceDate(newob.today())
        newid=newob.generateNewId()
        parent.manage_renameObjects(('copy_of_'+self.getId(),), (newid,))
        return parent.absolute_url()+'/'+newid

registerType(Invoice, PROJECTNAME)
