from plone.contentrules.engine.interfaces import IRuleStorage
from plone.app.workflow.remap import remap_workflow
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
    remap_workflow(site,
                   type_ids=('Document', 'Folder', 'Topic'),
                   chain=('intranett_workflow',))


def disable_contentrules(site):
    rule = queryUtility(IRuleStorage)
    if rule is not None:
        rule.active = False


def various(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('intranett-policy-various.txt') is None:
        return
    site = context.getSite()
    setup_locale(site)
    ensure_workflow(site)
    disable_contentrules(site)
