import urllib
from zope import interface
from Products import Five
from DateTime import DateTime
from Products.CMFCore import utils as cmf_utils
from Products.Extropy import permissions
from Products.CMFCore.utils import _checkPermission

class ITaskEdit(interface.Interface):
    def canEdit():
        """Return report data.
        """

    def hasTitle():
        """True if there is a title, used for displaying edit field"""

    def hasText():
        """True if there is text, used for displaying edit field"""

    def getRawText():
        """Return raw text for edit if the user has permission"""

    def getText():
        """Return formatted text for display"""

class TaskEdit(Five.BrowserView):
    """Helper view for task editing
    """

    def __init__(self, context, request):
        Five.BrowserView.__init__(self, context, request)

    def canEdit(self):
        # Initialize instead of dynamic lookup each access
        editable = getattr(self,'is_editable', None)
        if editable is None:
            self.is_editable = editable = _checkPermission('Modify portal content', self.context)
        return editable

    def hasTitle(self):
        return not not self.context.getRawTitle()

    def hasText(self):
        return not not self.context.getRawText()

    def getRawText(self):
        if self.canEdit():
            return self.context.getRawText()
        return None

    def getText(self):
        return self.context.getText()


class IDeliverableEdit(ITaskEdit):
    pass

class DeliverableEdit(TaskEdit):
    pass
