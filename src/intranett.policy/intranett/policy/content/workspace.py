from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from borg.localrole.interfaces import ILocalRoleProvider
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import WorkflowException
from zope.component import adapts
from zope.container.interfaces import IObjectRemovedEvent, IObjectAddedEvent
from zope.interface import implements
from plone.indexer.decorator import indexer

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
    security = ClassSecurityInfo()

    members = atapi.ATFieldProperty("members")

    security.declareProtected(ModifyPortalContent, 'setMembers')
    def setMembers(self, value):
        """Make sure the current user is always included."""
        user_id = getSecurityManager().getUser().getId()
        if user_id not in value:
            value = (user_id,) + tuple(value)
        self.Schema().getField('members').set(self, value)

    security.declareProtected(View, 'getWorkspace')
    def getWorkspace(self):
        """Return the closest workspace"""
        return self

    security.declareProtected(View, 'getWorkspaceState')
    def getWorkspaceState(self):
        """Return if the workspace is private or public"""
        return self.portal_workflow.getInfoFor(self, "review_state")


registerATCT(TeamWorkspace, PROJECTNAME)


@indexer(ITeamWorkspace)
def workspaceMembers(context):
    return context.members


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


def reindexChildren(context, action):
    reindexObjectsByPaths(context, ["/".join(context.getPhysicalPath())])


def reindexObjectsByPaths(context, paths):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    traverse = portal.restrictedTraverse
    for path in paths:
        o = traverse(path, None)
        if o is not None:
            o.reindexObjectSecurity()
        if getattr(o, 'isPrincipiaFolderish', None):
            subobject_paths = ["%s/%s" % (path, id) for id in o]
            reindexObjectsByPaths(context, subobject_paths)

