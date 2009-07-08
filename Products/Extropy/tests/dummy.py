from AccessControl import ClassSecurityInfo
from Products.Extropy.interfaces import IExtropyBase

from Products.Archetypes.public import *

schema = BaseSchema + Schema((
    StringField('budgetCategory',),
    ))

class ExtropyBase(BaseContent):
    """A simple type with budget category """
    schema = schema
    __implements__ = BaseContent.__implements__+(IExtropyBase,)

    security = ClassSecurityInfo()

registerType(ExtropyBase)

class ExtropyFolder(BaseFolder):
    """A simple folderish archetype"""
    schema = schema
    __implements__ = BaseContent.__implements__+(IExtropyBase,)

    security = ClassSecurityInfo()

registerType(ExtropyFolder)
