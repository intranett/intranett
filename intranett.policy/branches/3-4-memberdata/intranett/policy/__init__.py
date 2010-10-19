#

def unconfigure_can_review():
    # unconfigure the 'can review' utility the hard way
    from plone.app.workflow.interfaces import ISharingPageRole
    from zope.component import getGlobalSiteManager
    sm = getGlobalSiteManager()
    review = sm.queryUtility(ISharingPageRole, name=u'Reviewer')
    if review is not None:
        sm.unregisterUtility(provided=ISharingPageRole, name=u'Reviewer')


def initialize(context):
    unconfigure_can_review()
