from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Extropy.config import *
from Products.Extropy.content.ExtropyTracking import ExtropyTracking
from Products.Extropy.content.ExtropyBase import ExtropyBase, ExtropyBaseSchema, ParticipantsSchema

from Products.Extropy.interfaces import IExtropyBase

JarSchema = ExtropyBaseSchema + ParticipantsSchema

class ExtropyJar(ExtropyTracking, ExtropyBase, BaseFolder):
    """A Bug Jar contains Bugs, which are reported defects in a project."""
    schema = JarSchema
    implements(IExtropyBase)

    security = ClassSecurityInfo()

    def getBugs(self, **kw):
        """get contained bugs"""
        pass

    def getOpenBugs(self, **kw):
        """convenience"""
        pass

    def getMyOpenBugs(self):
        """even more convenient"""
        pass


registerType(ExtropyJar, PROJECTNAME)
