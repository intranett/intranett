from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

from config import OPEN_STATES
from interfaces import IExtropyFeature

def taskAddedSubscriber(task, event):
    """On task creation, set 'All tasks complete' to 'open' again"""
    deliverable = event.newParent
    if not IExtropyFeature.isImplementedBy(deliverable):
        return # Not added to a deliverable

    wftool = getToolByName(deliverable, 'portal_workflow', None)
    if not wftool:
        return # No context

    if wftool.getInfoFor(deliverable, 'review_state') != 'taskscomplete':
        return # Not in the tasks complete state

    if wftool.getInfoFor(task, 'review_state') not in OPEN_STATES:
        return # Not an open task

    wftool.doActionFor(deliverable, 'reopen')
