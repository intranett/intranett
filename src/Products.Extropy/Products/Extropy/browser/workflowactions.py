from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName


class WorkflowActions(BrowserView):

    def data(self):
        context = self.context
        wft = getToolByName(context, 'portal_workflow')
        state = wft.getInfoFor(context, 'review_state', None)

        putils = getToolByName(context, 'plone_utils')
        title = putils.getReviewStateTitleFor(context)
        return dict(state=state, title=title)


class RecordWorkflowActions(BrowserView):

    def data(self):
        state = self.context.review_state
        return dict(state=state, title=state)
