from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Extropy.interfaces import IExtropyBase

from Products.Archetypes.public import *

schema = BaseSchema + Schema((
    StringField('budgetCategory',),
    ))

class ExtropyBase(BaseContent):
    """A simple type with budget category """
    schema = schema
    implements(IExtropyBase)

    security = ClassSecurityInfo()

registerType(ExtropyBase)

class ExtropyFolder(BaseFolder):
    """A simple folderish archetype"""
    schema = schema
    implements(IExtropyBase)

    security = ClassSecurityInfo()

registerType(ExtropyFolder)
