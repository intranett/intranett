from zope.event import notify
from AccessControl import ModuleSecurityInfo
from Products.CMFCore.WorkflowCore import ActionSucceededEvent


def notifyActionSucceeded(state_change):
    """Called from workflow after scripts."""

    notify(ActionSucceededEvent(state_change.object,
                                state_change.workflow,
                                state_change.transition.getId(),
                                None))


# Allow from Python scripts
security = ModuleSecurityInfo('intranett.policy.workflow')
security.declarePublic('notifyActionSucceeded')
