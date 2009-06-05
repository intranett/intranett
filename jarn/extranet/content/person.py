from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.Archetypes.public import BaseSchema, Schema, BaseContent, \
     StringField, StringWidget, registerType, LinesField, \
     MultiSelectionWidget

from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import IUserAuthentication
from Products.membrane.interfaces import IPropertiesProvider
from Products.membrane.interfaces import IGroupsProvider
from Products.membrane.interfaces import IUserRoles
from Products.membrane.interfaces import IUserRelated
from Products.membrane.interfaces import IGroupAwareRolesProvider
from Products.membrane.utils import getFilteredValidRolesForPortal
from borg.localrole.interfaces import ILocalRoleProvider

from jarn.extranet.customer.config import PROJECTNAME
from jarn.extranet.customer.interfaces import IPerson

PersonSchema = BaseSchema + Schema((
    StringField('userName',
                languageIndependent = 1,
                widget = StringWidget(description = "Username for a person.")
               ),
    StringField('password',
                languageIndependent = 1,
                widget = StringWidget(description = "Password.")
               ),
    StringField('fullname',
                languageIndependent = 1,
                #schemata='userinfo',
                user_property=True,
                widget = StringWidget(description = "Full name.")
               ),

    ))


class LocalRoles(object):
    """Provide a local role manager for groups
    """
    implements(ILocalRoleProvider)

    def __init__(self, context):
        self.context = context

    def getAllRoles(self):
        user = IUserRelated(self.context)
        yield (user.getUserId(), ('Owner',))

    def getRoles(self, principal_id):
        for (pid,roles) in self.getAllRoles():
            if pid == principal_id:
                for r in roles:
                    yield r

class Person(BaseContent):
    """A person related to Jarn, can be a user"""
    schema = PersonSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    implements(IPerson, IUserAuthProvider, IUserAuthentication, IPropertiesProvider,
               IGroupsProvider, IGroupAwareRolesProvider, IUserRoles)

    getRoleSet = getFilteredValidRolesForPortal

    #
    # IUserAuthentication implementation
    # 'getUserName' is auto-generated
    #
    def verifyCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')
        if login == self.getUserName() and password == self.getPassword():
            return True
        else:
            return False

    def getRoles(self):
        return []


registerType(Person, PROJECTNAME)
