from zope.interface import Interface


class IExtropyBase(Interface):
    """ Interface for all real Extropy Objects """

    def getExtropyParent():
        """ Get first containing object that is an ExtropyProject"""


class IExtropyTracking(Interface):
    """
    Interface for object that can track tasks
    """


class IExtropyProject(Interface):
    """ Interface for projects """

    def getActivePhases():
        """ get the currently open phases"""


class IExtropyPhase(Interface):
    """
    Interface for Phase
    """


class IExtropyTrackingTool(Interface):
    """ Interface for the Extropy Tracking TOOL"""

    def trackingQuery(node, REQUEST=None, **kw):
        """ get items in subtree"""

    def localQuery(node,REQUEST=None, **kw):
        """ get items in subtree"""


class IExtropyTimeTrackingTool(Interface):
    """ Interface for the Extropy Tracking TOOL"""

    def localQuery(node=None,REQUEST=None, **kw):
        """ get items in subtree"""
