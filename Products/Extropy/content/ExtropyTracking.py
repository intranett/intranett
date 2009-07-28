from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.Extropy.interfaces import IExtropyTracking
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager

from Products.Extropy.config import *
from Products.Extropy.utils import dictifyBrain


class ResultList(list):
    def setTasksByState(self, dictionary):
        self.tasks_by_state = dictionary

    def getTasksByState(self):
        return getattr(self, 'tasks_by_state', {})


class ExtropyTracking:
    """Base class for types tracking tasks, requirements and bugs"""

    __implements__ = (IExtropyTracking)

    def getTasks(self, **kw):
        """gets all contained tasks, query by keywords"""
        ETTool = getToolByName(self,'extropy_tracking_tool')
        return ETTool.localQuery(self,REQUEST=None, portal_type='ExtropyTask', **kw)

    def getActivities(self, **kw):
        """gets all contained activities, query by keywords"""
        ETTool = getToolByName(self,'extropy_tracking_tool')
        return ETTool.localQuery(self,REQUEST=None, portal_type='ExtropyActivity', **kw)

    def getTasksByState(self,**kw):
        """gets all contained tasks, query by keywords"""
        ETTool = getToolByName(self,'extropy_tracking_tool')
        rawtasks = ETTool.localQuery(self,REQUEST=None, portal_type='ExtropyTask', **kw)
        tasks_by_state = {} # keyed by review_state
        tasks = ResultList()
        for task in rawtasks:
            tdict = dictifyBrain(task)
            tasks.append(tdict)
            tbs = tasks_by_state.get(task.review_state,[]) # get existing tasks for this state
            tbs.append(tdict) # add the last task
            tasks_by_state[task.review_state] = tbs #add the list back in
        tasks.setTasksByState(tasks_by_state)
        return tasks

    def getRequirementsByState(self,**kw):
        """ requirements by states"""
        ETTool = getToolByName(self,'extropy_tracking_tool')
        rawrequirements = ETTool.localQuery(self,REQUEST=None, portal_type='ExtropyFeature', **kw)
        requirements_by_state = {} # keyed by review_state
        requirements = ResultList()
        for requirement in rawrequirements:
            tdict = dictifyBrain(requirement)
            requirements.append(tdict)
            tbs = requirements_by_state.get(requirement.review_state,[]) # get existing requirements for this state
            tbs.append(tdict) # add the last requirement
            requirements_by_state[requirement.review_state] = tbs #add the list back in
        requirements.setTasksByState(requirements_by_state)
        return requirements

    def getTasksForCurrentUser(self, **kw):
        """convenience"""
        curruser = getSecurityManager().getUser().getUserName()
        ETTool = getToolByName(self,'extropy_tracking_tool')
        return self.getTasks(getResponsiblePerson=curruser, **kw)

    def getDeliverables(self, **kw):
        ETTool = getToolByName(self,'extropy_tracking_tool')
        return ETTool.localQuery(self,REQUEST=None, portal_type='ExtropyFeature', **kw)

    def getRequirements(self, **kw):
        """get contained features"""
        print "getRequirements is deprecated, use getDeliverables instead"
        return self.getDeliverables(**kw)

    def countTasks(self):
        """the number of tasks total"""
        return len(self.getTasks())

    def countOpenTasks(self):
        """the number of 'open' tasks total"""
        ETTool = getToolByName(self,'extropy_tracking_tool')
        return len(self.getTasks(review_state=ETTool.getOpenStates()))

    def getWorkedTime(self):
        """get the total amount of time worked for this object"""
        tool = getToolByName(self,TIMETOOLNAME)
        return tool.countIntervalHours(node=self)

    def getRemainingTime(self):
        tool = getToolByName(self,'extropy_tracking_tool')
        tasks = tool.localQuery(self, REQUEST=None, portal_type=['ExtropyTask', 'ExtropyActivity'])
        if tasks is None or len(tasks)==0 or not tasks:
            return 0
        return reduce(lambda x, y: x + y , [t.getRemainingTime for t in tasks])
