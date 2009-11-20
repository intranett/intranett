from zope.interface import Interface


class IExtropyBase(Interface):
    """ Interface for all real Extropy Objects """

    def getExtropyParent():
        """ Get first containing object that is an ExtropyProject"""


class IExtropyTracking(Interface):
    """
    Interface for object that can track tasks
    """
    def getTasks(**kw):
        """gets all contained tasks, limited by parameters"""

    def getTasksForCurrentUser(**kw):
        """getTasks, only limited to tasks owned by the current user"""


class IExtropyProject(Interface):
    """ Interface for projects """

    def getActivePhases():
        """ get the currently open phases"""


class IExtropyPhase(Interface):
    """
    Interface for Phase
    """

    def getTasks(**kw):
        """Get all contained tasks"""

    def getTargetFeatures():
        """get all features targetted for finishing this phase"""

    def getTargetBugs():
        """ get bugs targetted for fixing this pase"""


class IExtropyTask(Interface):
    """
    Interface for tasks
    """

    def moveTo(uid):
        """
        move task to a different phase
        targetphase should be an UID
        """

    def getOriginatingFeature():
        """
        The originating feature
        """


class IExtropyBugJar(Interface):
    """
    Interface
    """
    def getBugs(**kw):
        """
        get all contained features
        filter by **kw
        """

    def getBugsWithTasks(**kw):
        """
        get all contained features, filtered by **kw,
        and all linked tasks for each feature
        """


class IExtropyBug(Interface):
    """
    Interface
    """

    def spawnTask(targetphase=None):
        """
            Make a new task with a reference to this bug
            The task is created inside targetphase or in the currently active phase
            Important properties of the feature (nosy list etc) are copied to the task
        """

    def getSpawnedTasks():
        """return all linked tasks"""


class IExtropyFeature(Interface):
    """
        A user story,
        a project feature,
        something that must be accomplished for the customer
    """
    def spawnTask(targetphase=None):
        """
            Make a new task with a reference to this feature
            The task is created inside targetphase or in the currently active phase
            Important properties of the feature (nosy list etc) are copied to the task
        """

    def getSpawnedTasks():
        """return all linked tasks"""


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

class IExtropyPlan(Interface):
    """ Interface for the (weekly) plan
    A plan is for a certain user and has references to deliverables and tasks
    that are supposed to be completed in the duration of the plan"""

    def addItem(item, **kw):
        """ Add item to the plan
        This is only allowed before the plan is approved"""

    def deleteItem(item):
        """ Remove an item from the plan - can only be done
        before approval """

    def getItems():
        """ Get all the planned items """

    def addAdditionalItem(item, **kw):
        """ Add additional item to the plan
        This is used for extra  items done after approval"""

    def deleteAdditionalItem(item):
        """ Remove an item from the plan - can only be done
        before approval """

    def getAdditionalItems():
        """ Get all the items added after approval """
