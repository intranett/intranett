from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class FrontpageView(BrowserView):
    """
    Frontpage view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

