from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.viewlet.interfaces import IViewlet


class NoDatepicker(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(NoDatepicker, self).__init__(context, request, view, manager)
        self.view = view
        self.manager = manager

    def update(self):
        pass

    def render(self):
        return u""
