from AccessControl import getSecurityManager
from borg.localrole.interfaces import ILocalRoleProvider
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import WorkflowException
from zope.component import adapts
from zope.container.interfaces import IObjectRemovedEvent, IObjectAddedEvent
from zope.interface import implements

from intranett.policy import IntranettMessageFactory as _
from intranett.policy.config import PROJECTNAME
from intranett.policy.interfaces import ITeamWorkspace

WorkspaceSchema = ATFolder.schema.copy() + atapi.Schema((
    atapi.LinesField(
        'members',
        required=False,
        multiValued=True,
        vocabulary_factory='intranett.policy.WorkspaceMemberVocabulary',
        storage=atapi.AnnotationStorage(),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Members"),
            description=_(u"Users who have access to the workspace"),
            format='checkbox',
        ),
    ),
))


class TeamWorkspace(ATFolder):
    """A workspace for groups of members"""

    implements(ITeamWorkspace)
    schema = WorkspaceSchema
    meta_type = "TeamWorkspace"

    members = atapi.ATFieldProperty("members")

    def getWorkspace(self):
        """Return the closest workspace"""
        return self

    def getWorkspaceState(self):
        """Return if the workspace is private or public"""
        return self.portal_workflow.getInfoFor(self, "review_state")


registerATCT(TeamWorkspace, PROJECTNAME)


class WorkspaceMembershipRoles(object):
    """Gives members of a TeamWorkspace appropriate roles in context"""
    implements(ILocalRoleProvider)
    adapts(ITeamWorkspace)

    def __init__(self, context):
        self.context = context

    def getRoles(self, principal_id):
        if principal_id in self.context.members:
            return ['Member', 'Editor', 'Contributor']
        else:
            return []

    def getAllRoles(self):
        return [(member, self.getRoles(member)) for member in self.context.members]


def addCreatorToMembers(context, action):
    """Make sure the current user cannot remove himself."""
    user = getSecurityManager().getUser().getId()
    if user not in context.members:
        context.members = (user,) + context.members


def triggerAutomaticTransitions(context, action):
    if IObjectAddedEvent.providedBy(action):
        return
    if IObjectRemovedEvent.providedBy(action):
        return

    wf = getattr(context, 'portal_workflow', None)
    try:
        wf.doActionFor(context, "noop")
    except (WorkflowException, AttributeError):
        pass


def transitionChildren(context, action):
    if action.action == "publish":
        subaction = "unprotect"
    elif action.action == "hide":
        subaction = "protect"
    else:
        return None
    context.REQUEST.method= "POST"
    transitionObjectsByPaths(context, subaction, ["/".join(context.getPhysicalPath())])


def transitionObjectsByPaths(context, workflow_action, paths):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    traverse = portal.restrictedTraverse
    for path in paths:
        o = traverse(path, None)
        if o is not None:
            try:
                o.portal_workflow.doActionFor(o, workflow_action)
            except WorkflowException:
                # We might be beaten to the punch by automatic transitions
                # but as long as the tests pass we know we're not missing
                # things here
                pass
        if getattr(o, 'isPrincipiaFolderish', None):
            subobject_paths = ["%s/%s" % (path, id) for id in o]
            transitionObjectsByPaths(context, workflow_action, subobject_paths)
    return

