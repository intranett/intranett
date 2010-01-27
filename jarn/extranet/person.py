from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.Archetypes.public import BaseSchema, Schema, BaseContent, \
     StringField, StringWidget, registerType, LinesField, \
     MultiSelectionWidget, ImageField, ImageWidget

from jarn.extranet.config import PROJECTNAME
from jarn.extranet.interfaces import IPerson

PersonSchema = BaseSchema + Schema((
    StringField('title',
                accessor='Title',
                languageIndependent = 1,
                #schemata='userinfo',
                user_property=True,
                widget = StringWidget(description = "Full name.")
               ),
    StringField('userName',
                languageIndependent = 1,
                widget = StringWidget(description = "Username for a person.")
               ),
    StringField('password',
                languageIndependent = 1,
                widget = StringWidget(description = "Password.")
               ),
    ImageField('photo',
        widget=ImageWidget(label='Photo')
        ),



    ))
        



class Person(BaseContent):
    """A person related to Jarn, can be a user"""
    implements(IPerson)
    
    schema = PersonSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()


    def verifyCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')
        if login == self.getUserName() and password == self.getPassword():
            return True
        else:
            return False

registerType(Person, PROJECTNAME)
