from plone.app.portlets.dashboard import DefaultDashboard
from plone.app.users.userdataschema import checkEmailAddress
from plone.app.users.userdataschema import IUserDataSchemaProvider
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

    description = schema.Text(
        title=_(u'label_biography', default=u'Biography'),
        description=_(u'help_biography',
                      default=u"A short overview of who you are and what you "
                      "do. Will be displayed on your author page, linked "
                      "from the items you create."),
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
                      'Recommended image size is 75 pixels wide by 100 '
                      'pixels tall.'),
        required=False)

    pdelete = schema.Bool(
        title=_(u'label_delete_portrait', default=u'Delete Portrait'),
        description=u'',
        required=False)


class UserDataSchemaProvider(object):

    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return ICustomUserDataSchema


class CustomDefaultDashboard(DefaultDashboard):

    def __call__(self):
        return {
            'plone.dashboard1': (),
            'plone.dashboard2': (),
            'plone.dashboard3': (),
            'plone.dashboard4': (),
        }
