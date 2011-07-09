from zope.interface import Interface


class IMembersFolder(Interface):
    """MembersFolder marker interface."""


class IMembersFolderId(Interface):
    """A MembersFolder registers its id as a utility."""


class IProjectRoom(Interface):
    """ProjectRoom marker interface."""
