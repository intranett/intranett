from itertools import groupby, chain
from operator import itemgetter

from persistent import Persistent
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.interface import implements

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.Extropy.config import TOOLNAME, OPEN_STATES


class IMyResponsibilitiesPortlet(IPortletDataProvider):
    """A portlet which renders work hours.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMyResponsibilitiesPortlet)
    title = "My Responsibilities"


def _reconstructURL(parent, child):
    # Reconstruct the URL of an item one step deeper from the parent's URL
    # but one or more steps shallower than the child's URL.
    parentURL = parent.get('getURL')
    childURL = child.get('getURL')
    if not parentURL or not childURL:
        return ''
    next_step = childURL[len(parentURL) + 1:].split('/', 1)[0]
    url = '%s/%s' % (parentURL, next_step)
    return url


class ItemsTree(Persistent):
    """Builds a tree from catalog items
    """

    def __init__(self, records):
        self.data = []
        for record in records:
            copy = dict((k, getattr(record, k))
                        for k in record.__record_schema__.keys())
            copy['getURL'] = record.getURL()
            copy['getPath'] = record.getPath()
            self.data.append(copy)
        self.data.sort(key=lambda d: (
            d['getProjectTitle'].lower(), d['getPhaseTitle'].lower(),
            d['getDeliverableTitle'].lower(),
            d['portal_type'] in ('ExtropyTask', 'ExtropyActivity') and
                d['Title'].lower() or ''))

    def __iter__(self):
        for (prtitle, pritems) in groupby(
            self.data, itemgetter('getProjectTitle')):
            # Yield a project, or reconstruct enough info
            project = pritems.next()

            next = [] # Used to put iterated item back into flow
            if project['portal_type'] != 'ExtropyProject':
                next = [project]
                project = dict(Title=prtitle)
            project['depth'] = 0
            yield project

            for (phtitle, phitems) in groupby(
                chain(next, pritems), itemgetter('getPhaseTitle')):
                # Reconstruct enough info for a phase
                next = [phitems.next()]
                phase = dict(depth=1, Title=phtitle,
                             getURL=_reconstructURL(project, next[0]))
                yield phase

                for (dtitle, tasks) in groupby(
                    chain(next, phitems), itemgetter('getDeliverableTitle')):
                    # Yield a deliverable, at least the title
                    deliverable = tasks.next()

                    next = [] # Used to put iterated item back into flow
                    if deliverable['portal_type'] != 'ExtropyFeature':
                        next = [deliverable]
                        if not dtitle:
                            # Activities live in the phase, group together
                            deliverable = dict(Title='Activities',
                                               getURL=phase['getURL'])
                        else:
                            deliverable = dict(
                                Title=dtitle,
                                getURL=_reconstructURL(phase, deliverable))
                    deliverable['depth'] = 2
                    yield deliverable

                    for item in chain(next, tasks):
                        item['depth'] = 3
                        yield item


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    available = True
    render = ViewPageTemplateFile('myresponsibilitiesportlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()

    def fetchData(self):
        """Gets the item data."""
        etool = getToolByName(self, TOOLNAME)
        user = getSecurityManager().getUser().getUserName()
        projects = etool.searchResults(
            portal_type='ExtropyProject',
            getParticipants=user,
            review_state='active')
        items = etool.searchResults(
            portal_type=('ExtropyActivity', 'ExtropyFeature',
                         'ExtropyTask'),
            getResponsiblePerson=user,
            review_state=OPEN_STATES)
        return ItemsTree(list(projects) + list(items))

    def reportlink(self):
        "link to the more detailed view"
        return "%s/weeklyplan_report" % (self.portal_url, )


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
