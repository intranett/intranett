from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from borg.localrole.interfaces import ILocalRoleProvider
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.permission import ChangeEvents
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import WorkflowException
from zope.interface import implements
from zope.component import getUtility, adapts
from zope.schema.interfaces import IVocabularyFactory
from zope.container.interfaces import IObjectRemovedEvent, IObjectAddedEvent
from plone.indexer.decorator import indexer

from intranett.policy import IntranettMessageFactory as _
from intranett.policy.config import PROJECTNAME
from intranett.policy.interfaces import ITeamWorkspace

WorkspaceSchema = ATFolder.schema.copy() + atapi.Schema((
    atapi.LinesField(
        'members',
        required=False,
        multiValued=True,
        vocabulary='getMembersVocabulary',
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

    security.declarePrivate('membersource')
    @property
    def membersource(self):
        return getUtility(IVocabularyFactory, name="plone.principalsource.Principals")(self)

    security.declarePrivate('userInMemberSource')
    def userInMemberSource(self, user_id):
        """Return true if user_id is in member source."""
        try:
            self.membersource.getTermByToken(user_id)
        except LookupError:
            return False
        return True

    security.declarePrivate('getMembersVocabulary')
    def getMembersVocabulary(self):
        """Return user_id -> fullname DisplayList."""
        # We cannot use 'vocabulary_factory' on the field as this would
        # result in a login -> fullname DisplayList.
        return atapi.DisplayList((t.token, t.title) for t in self.membersource)

    security.declareProtected(ModifyPortalContent, 'setMembers')
    def setMembers(self, value):
        """Make sure the current user is always included."""
        user_id = getSecurityManager().getUser().getId()
        value = list(value)
        if user_id not in value and self.userInMemberSource(user_id):
            value.append(user_id)
        value.sort()
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
            return ['Editor', 'Contributor']
        else:
            return []

    def getAllRoles(self):
        return [(member, self.getRoles(member)) for member in self.context.members]


def transitionChildren(context, action):
    """Transition children when the workspace state has changed."""
    if action.action in ('publish', 'hide'):
        transitionObjectsByPaths(context, 'auto', ['/'.join(context.getPhysicalPath())])


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
    """Reindex children when the workspace membership has changed."""
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


def transitionMovedContent(context, action):
    """Transition objects when they have been moved."""
    if IObjectAddedEvent.providedBy(action):
        return
    if IObjectRemovedEvent.providedBy(action):
        return

    wf = getattr(context, 'portal_workflow', None)

    if getattr(action.oldParent, 'getWorkspaceState', None) is not None:
        if getattr(action.newParent, 'getWorkspaceState', None) is None:
            # If an object is moved out of a workspace, take ownership.
            becomeOwner(context)
            restoreOwnerPermissions(context)

            # If it uses the intranett_workflow, also hide it.
            if 'intranett_workflow' in wf.getChainFor(context):
                wf.doActionFor(context, "hide")
                return
        else:
            # If an object is renamed inside a workspace or moved between
            # workspaces, reapply removeOwnerPermissions.
            if wf.getInfoFor(context, 'review_state') == 'published':
                action.action = 'autopublish' # Abuse existing event
                removeOwnerPermissions(context, action)
                return

    # In all other cases the automatic transitions do the right thing
    wf.doActionFor(context, "auto")


def removeOwnerPermissions(context, action):
    """Remove owner permissions when an object is published in a workspace."""
    if action.action in ('autopublish',):
        if getattr(context, 'getWorkspaceState', None) is not None:
            for perm in (View, AccessContentsInformation,
                         ModifyPortalContent, ChangeEvents):
                try:
                    roles = context.rolesOfPermission(perm)
                except ValueError:
                    pass # Only Folders have 'Change portal events'
                else:
                    roles = [x['name'] for x in roles if x['selected']]
                    if 'Owner' in roles:
                        roles.remove('Owner')
                        context.manage_permission(perm, roles, acquire=0)


def becomeOwner(context):
    """Become the object's owner (in local role terms)."""
    user_id = getSecurityManager().getUser().getId()
    owners = context.users_with_local_role('Owner')

    for owner_id in owners:
        roles = context.get_local_roles_for_userid(owner_id)
        roles = [x for x in roles if x != 'Owner']
        if roles:
            context.manage_setLocalRoles(owner_id, roles)
        else:
            context.manage_delLocalRoles([owner_id])

    roles = context.get_local_roles_for_userid(user_id)
    if 'Owner' not in roles:
        roles += ('Owner',)
        context.manage_setLocalRoles(user_id, roles)


def restoreOwnerPermissions(context):
    """Restore owner permissions."""
    for perm in (View, AccessContentsInformation,
                 ModifyPortalContent, ChangeEvents):
        try:
            roles = context.rolesOfPermission(perm)
        except ValueError:
            pass # Only Folders have 'Change portal events'
        else:
            roles = [x['name'] for x in roles if x['selected']]
            if 'Owner' not in roles:
                roles.append('Owner')
                context.manage_permission(perm, roles, acquire=0)

