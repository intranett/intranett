from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Extropy.config import *

ExtropyHourGlassSchema = BaseSchema.copy()

class ExtropyHourGlass(BaseBTreeFolder):
    """An Hour Glass contains hours registered in a project."""

    schema = ExtropyHourGlassSchema

registerType(ExtropyHourGlass, PROJECTNAME)
