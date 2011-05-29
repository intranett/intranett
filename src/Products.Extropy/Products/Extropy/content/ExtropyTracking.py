from Products.CMFCore.utils import getToolByName
from zope.interface import implements

from Products.Extropy.config import TIMETOOLNAME
from Products.Extropy.interfaces import IExtropyTracking


class ExtropyTracking:
    """Base class for types tracking tasks, requirements and bugs"""

    implements(IExtropyTracking)

    def getActivities(self, **kw):
        """gets all contained activities, query by keywords"""
        ETTool = getToolByName(self,'extropy_tracking_tool')
        return ETTool.localQuery(self,REQUEST=None, portal_type='ExtropyActivity', **kw)

    def getWorkedTime(self):
        """get the total amount of time worked for this object"""
        tool = getToolByName(self,TIMETOOLNAME)
        return tool.countIntervalHours(node=self)

    def getUnbilledTime(self):
        """get the total amount of time worked for this object"""
        tool = getToolByName(self,TIMETOOLNAME)
        return tool.countIntervalHours(node=self, review_state='entered',  getBudgetCategory='Billable')
