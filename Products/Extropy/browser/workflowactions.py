from itertools import ifilter, imap

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionInformation import ActionInfo, oai
from Products.Five import BrowserView
from Products.PageTemplates.Expressions import getEngine
from Products.PageTemplates.Expressions import SecureModuleImporter

class WorkflowActions(BrowserView):
    actions = ()
    review_state = None
    review_state_title = None

    def __call__(self, *args, **kw):
        context = aq_inner(self.context)
        wft = getToolByName(context, 'portal_workflow')
        if 'action' in self.request:
            wft.doActionFor(context, self.request.action)
        self.actions = wft.listActionInfos(object=context)
        self.review_state = wft.getInfoFor(context, 'review_state', None)

        putils = getToolByName(context, 'plone_utils')
        self.review_state_title = putils.getReviewStateTitleFor(context)

        return super(WorkflowActions, self).__call__(*args, **kw)

# Workflow actions for catalog results (hold on to your pants, hackery ahead!)

# ActionProvider information objects, adjusted to catalog brains
class _RecordOAI(oai):
    """ActionInfo class for catalog records"""
    def __init__(self, object):
        utool = getToolByName(object, 'portal_url')

        membership = getToolByName(object, 'portal_membership')
        self.isAnonymous = membership.isAnonymousUser()
        self.user_id = membership.getAuthenticatedMember().getId()
        self.portal = self.folder = utool.getPortalObject()
        self.portal_url = self.folder_url = utool()
        self.object = self.content = object
        self.object_url = self.content_url = object.getURL()

def _getRecordExpressionContext(object, request):
    """ExpressionContext for catalog records"""
    utool = getToolByName(object, 'portal_url')
    membership = getToolByName(object, 'portal_membership')
    if membership.isAnonymousUser():
        member = None
    else:
        member = membership.getAuthenticatedMember()
    portal = utool.getPortalObject()
    portal_url = utool()

    data = dict(
        object_url=object.getURL(),
        folder_url=portal_url,
        portal_url=portal_url,
        object=object,
        folder=portal,
        nothing=None,
        request=request,
        modules=SecureModuleImporter,
        member=member
    )
    return getEngine().getContext(data)

class WFHistoryWrapper:
    """Wrapper for records providing wfhistory info"""
    def __init__(self, record, state, wf_id, state_var):
        self._record = record
        self.workflow_history = {wf_id: ({state_var: state},)}

    def __getattr__(self, key):
        return getattr(self._record, key)

# Workflow actions for records
# it won't do transitions, use a regular WorkflowActions view for that
# Note that transition guards are basically ignored, as no security context
# (of any consequence) is available.
class RecordWorkflowActions(BrowserView):

    def _workflows(self):
        context = aq_inner(self.context)
        tool = getToolByName(context, 'portal_workflow')
        chain = tool.getChainFor(context.portal_type)
        return ifilter(None, imap(tool.getWorkflowById, chain))

    @property
    def review_state_title(self):
        review_state = aq_inner(self.context).review_state
        for wf in self._workflows():
            if wf.states.has_key(review_state):
                return wf.states[review_state].title or review_state
        return None

    @property
    def actions(self):
        context = aq_inner(self.context)
        econtext = _getRecordExpressionContext(context, self.request)
        review_state = context.review_state
        for wf in self._workflows():
            record = WFHistoryWrapper(context, review_state, wf.getId(),
                                      wf.state_var)
            oai = _RecordOAI(record)
            for action in ifilter(None, wf.listObjectActions(oai)):
                ainfo = ActionInfo(action, econtext)
                if not ainfo['visible']:
                    continue
                if not ainfo['allowed']:
                    continue
                if not ainfo['available']:
                    continue
                yield ainfo
