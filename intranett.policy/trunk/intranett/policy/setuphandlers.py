from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility


def setup_locale(site):
    site.setLanguage('no')

    tool = getToolByName(site, "portal_languages")
    tool.manage_setLanguageSettings('no',
        ['no'],
        setUseCombinedLanguageCodes=False,
        startNeutral=False)

    calendar = getToolByName(site, "portal_calendar")
    calendar.firstweekday = 0


def ensure_workflow(site):
    # Force the default content into the correct workflow
    from plone.app.workflow.remap import remap_workflow
    remap_workflow(site,
                   type_ids=('Document', 'Folder', 'Topic'),
                   chain=('intranett_workflow', ))


def disable_contentrules(site):
    from plone.contentrules.engine.interfaces import IRuleStorage
    rule = queryUtility(IRuleStorage)
    if rule is not None:
        rule.active = False


def disallow_sendto(site):
    perm_id = 'Allow sendto'
    site.manage_permission(perm_id, roles=['Manager'], acquire=0)


def disable_collections(site):
    # Once collections are usable or we have a SiteAdmin role this should be
    # changed (both depend on Plone 4.1)
    perm_id = 'Add portal topics'
    site.manage_permission(perm_id, roles=[], acquire=0)
    perm_id = 'plone.portlet.collection: Add collection portlet'
    site.manage_permission(perm_id, roles=[], acquire=0)


def disable_portlets(site):
    from plone.portlets.interfaces import IPortletType
    from zope.component import getUtilitiesFor

    disabled = ['portlets.Calendar', 'portlets.Classic', 'portlets.Login',
                'portlets.Review']

    for info in getUtilitiesFor(IPortletType):
        if info[0] in disabled:
            p = info[1]
            # We remove the IColumn specification here, which makes the
            # portlets not addable for anything
            p.for_ = []
            p._p_changed = True


def setup_default_groups(site):
    gtool = getToolByName(site, 'portal_groups')
    # We could add more groups like this:
    # gtool.addGroup('Users', title='Users', roles=['Member'])
    gtool.removeGroups(['Administrators', 'Reviewers'])


def various(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('intranett-policy-various.txt') is None:
        return
    site = context.getSite()
    setup_locale(site)
    ensure_workflow(site)
    disable_contentrules(site)
    disallow_sendto(site)
    disable_collections(site)
    disable_portlets(site)
    setup_default_groups(site)
