from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class WorkflowActions(BrowserView):

    def data(self):
        context = aq_inner(self.context)
        wft = getToolByName(context, 'portal_workflow')
        state = wft.getInfoFor(context, 'review_state', None)

        putils = getToolByName(context, 'plone_utils')
        title = putils.getReviewStateTitleFor(context)
        return dict(state=state, title=title)
