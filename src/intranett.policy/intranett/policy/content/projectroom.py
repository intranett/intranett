from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from borg.localrole.interfaces import ILocalRoleProvider
from plone.indexer.decorator import indexer
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.permission import ChangeEvents
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from zope.schema.interfaces import IVocabularyFactory

from intranett.policy import IntranettMessageFactory as _
from intranett.policy.config import PROJECTNAME
from intranett.policy.interfaces import IProjectRoom

ProjectRoomSchema = ATFolder.schema.copy() + atapi.Schema((
    atapi.LinesField(
        'participants',
        required=False,
        multiValued=True,
        vocabulary='getParticipantsVocabulary',
        storage=atapi.AnnotationStorage(),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Participants"),
            description=_(u"Users who have access to the project room."),
            format='checkbox',
        ),
    ),
))


class ProjectRoom(ATFolder):
    """A project room for groups of participants"""

    implements(IProjectRoom)
    schema = ProjectRoomSchema
    meta_type = "ProjectRoom"
    security = ClassSecurityInfo()

    participants = atapi.ATFieldProperty("participants")

    security.declarePrivate('participantsource')
    @property
    def participantsource(self):
        return getUtility(IVocabularyFactory,
            name="plone.principalsource.Principals")(self)

    security.declarePrivate('userInParticipantSource')
    def userInParticipantSource(self, user_id):
        """Return true if user_id is in participant source."""
        try:
            self.participantsource.getTermByToken(user_id)
        except LookupError: # pragma: no cover
            return False
        return True

    security.declarePrivate('getParticipantsVocabulary')
    def getParticipantsVocabulary(self):
        """Return user_id -> fullname DisplayList."""
        # We cannot use 'vocabulary_factory' on the field as this would
        # result in a login -> fullname DisplayList.
        return atapi.DisplayList(
            (t.token, t.title) for t in self.participantsource)

    security.declareProtected(ModifyPortalContent, 'setParticipants')
    def setParticipants(self, value):
        """Make sure the current user is always included."""
        user_id = getSecurityManager().getUser().getId()
        value = list(value)
        if user_id not in value and self.userInParticipantSource(user_id):
            value.append(user_id)
        value.sort()
        self.Schema().getField('participants').set(self, value)

    security.declareProtected(View, 'getProjectRoom')
    def getProjectRoom(self):
        """Return the closest project room"""
        return self

    security.declareProtected(View, 'getProjectRoomState')
    def getProjectRoomState(self):
        """Return if the project room is private or public"""
        wftool = getToolByName(self, 'portal_workflow')
        return wftool.getInfoFor(self, "review_state")


registerATCT(ProjectRoom, PROJECTNAME)


@indexer(IProjectRoom)
def participants(context):
    return context.participants


class ProjectRoomParticipantRoles(object):
    """Gives participants of a ProjectRoom appropriate roles in context"""
    implements(ILocalRoleProvider)
    adapts(IProjectRoom)

    def __init__(self, context):
        self.context = context

    def getRoles(self, principal_id):
        if principal_id in self.context.participants:
            return ['Editor', 'Contributor']
        else:
            return []

    def getAllRoles(self):
        return [(participant, self.getRoles(participant)) for participant in
            self.context.participants]


def transitionChildren(context, action):
    """Transition children when the project room state has changed."""
    if action.action in ('publish', 'hide'):
        transitionObjectsByPaths(context, 'auto',
            ['/'.join(context.getPhysicalPath())])


def transitionObjectsByPaths(context, workflow_action, paths):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    traverse = portal.restrictedTraverse
    for path in paths:
        o = traverse(path, None)
        if o is not None:
            o.portal_workflow.doActionFor(o, workflow_action)
        if getattr(o, 'isPrincipiaFolderish', None):
            subobject_paths = ["%s/%s" % (path, id) for id in o]
            transitionObjectsByPaths(context, workflow_action, subobject_paths)


def reindexChildren(context, action):
    """Reindex children when the project participants have changed."""
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

    if getattr(action.oldParent, 'getProjectRoomState', None) is not None:
        if getattr(action.newParent, 'getProjectRoomState', None) is None:
            # If an object is moved out of a project room, take ownership.
            becomeOwner(context)
            restoreOwnerPermissions(context)

            # If it uses the intranett_workflow, also hide it.
            if 'intranett_workflow' in wf.getChainFor(context):
                wf.doActionFor(context, "hide")
                return
        else:
            # If an object is renamed inside a project room or moved between
            # project rooms, reapply removeOwnerPermissions.
            if wf.getInfoFor(context, 'review_state') == 'published':
                action.action = 'autopublish' # Abuse existing event
                removeOwnerPermissions(context, action)
                return

    # In all other cases the automatic transitions do the right thing
    wf.doActionFor(context, "auto")


def removeOwnerPermissions(context, action):
    """Remove owner permissions when an object is published in a project room
    """
    if action.action in ('autopublish',):
        if getattr(context, 'getProjectRoomState', None) is not None:
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
