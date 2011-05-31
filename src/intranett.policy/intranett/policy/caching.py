from zope.interface import implements
from zope.interface import Interface

from zope.component import adapts

from plone.app.caching.interfaces import IETagValue


class EditBarCookie(object):
    """The ``editbar`` etag component, returning the value of the
    editbar_opened cookie.
    """

    implements(IETagValue)
    adapts(Interface, Interface)

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        return self.request.cookies.get('editbar_opened', '0')


class WorkspaceState(object):
    """The ``workspace`` etag component, returning 1 if a containing
    workspace is private, 0 if it is public or if there is no workspace.
    """

    implements(IETagValue)
    adapts(Interface, Interface)

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        if getattr(self.published, 'getWorkspaceState', None) is not None:
            if self.published.getWorkspaceState() == 'private':
                return '1'
        return '0'
