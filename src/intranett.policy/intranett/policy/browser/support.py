from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.viewlet.interfaces import IViewlet


VIEWLET_TEXT = u"""
<script type="text/javascript" defer="defer"
  src="//asset0.zendesk.com/external/zenbox/v2.1/zenbox.js"></script>
<style type="text/css" media="screen, projection">
  @import url(//asset0.zendesk.com/external/zenbox/v2.1/zenbox.css);
</style>
<script type="text/javascript">
  if (typeof(Zenbox) !== "undefined") {
    Zenbox.init({
      dropboxID:   "20021871",
      url:         "https://jarn.zendesk.com",
      tabID:       "support",
      tabColor:    "#444",
      tabPosition: "Right"
    });
  }
</script>
"""


class SupportViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(SupportViewlet, self).__init__(context, request)
        self.view = view
        self.manager = manager

    def update(self):
        pass

    def render(self):
        return VIEWLET_TEXT
