from plone.app.portlets.dashboard import DefaultDashboard
from plone.app.users.userdataschema import checkEmailAddress
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from Products.CMFDefault.formlib.schema import FileUpload
from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements
from zope.interface import Interface
from zope import schema


class ICustomUserDataSchema(Interface):

    fullname = schema.TextLine(
        title=_(u'label_full_name', default=u'Full Name'),
        description=u'',
        required=False)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        required=True,
        constraint=checkEmailAddress)

    phone = schema.ASCIILine(
        title=_(u'label_phone', default=u'Phone'),
        description=_(u'help_phone',
                      default=u'Your company phone number.'),
        required=False)

    mobile = schema.ASCIILine(
        title=_(u'label_mobile', default=u'Mobile phone'),
        description=_(u'help_mobile',
                      default=u'Your mobile phone number.'),
        required=False)

    description = schema.Text(
        title=_(u'label_biography', default=u'Biography'),
        description=_(u'help_biography',
                      default=u"A short overview of who you are and what you "
                      "do. Will be displayed on your author page, linked "
                      "from the items you create."),
        required=False)

    department = schema.TextLine(
        title=_(u'label_department', default=u'Department'),
        description=_(u'help_department',
                      default=u"Your department in the company."),
        required=False)

    location = schema.TextLine(
        title=_(u'label_location', default=u'Location'),
        description=_(u'help_location',
                      default=u"Your location - either city and "
                      "country - or in a company setting, where "
                      "your office is located."),
        required=False)

    portrait = FileUpload(title=_(u'label_portrait', default=u'Portrait'),
        description=_(u'help_portrait',
                      default=u'To add or change the portrait: click the '
                      '"Browse" button; select a picture of yourself. '
                      'We recommend to upload a square image not smaller '
                      'than 300px wide by 300px tall.'),
        required=False)

    pdelete = schema.Bool(
        title=_(u'label_delete_portrait', default=u'Delete Portrait'),
        description=u'',
        required=False)


class UserDataSchemaProvider(object):

    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return ICustomUserDataSchema


class CustomUserDataPanelAdapter(UserDataPanelAdapter):

    def get_department(self):
        return self.context.getProperty('department', '')
    def set_department(self, value):
        self.context.setMemberProperties({'department': value})
    department = property(get_department, set_department)

    def get_phone(self):
        return self.context.getProperty('phone', '')
    def set_phone(self, value):
        self.context.setMemberProperties({'phone': value})
    phone = property(get_phone, set_phone)

    def get_mobile(self):
        return self.context.getProperty('mobile', '')
    def set_mobile(self, value):
        self.context.setMemberProperties({'mobile': value})
    mobile = property(get_mobile, set_mobile)


class CustomDefaultDashboard(DefaultDashboard):

    def __call__(self):
        return {
            'plone.dashboard1': (),
            'plone.dashboard2': (),
            'plone.dashboard3': (),
            'plone.dashboard4': (),
        }
