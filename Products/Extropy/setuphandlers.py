from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.ZCTextIndex.PipelineFactory import element_factory
from Products.ZCTextIndex.ZCTextIndex import PLexicon

from Products.Extropy import config


class Extra(object):
    pass


def tweakTimeTrackerActions(portal, out):
    """we need an extra action in the formcontroller for the redirects to work properly"""
    pfc = getToolByName(portal, 'portal_form_controller')
    pfc.addFormAction('validate_integrity',
                      'success',
                      'ExtropyHours',
                      '',
                      'redirect_to',
                      'string:workhours_statusmessage')

def setupCatalogMultiplex(portal, out):
    """ better than overriding all the index-methods, and more flexible too"""
    trackingtypes = ['ExtropyFeature', 'ExtropyTask', 'ExtropyBug', 'ExtropyActivity']
    remainingtypes = ['ExtropyProject', 'ExtropyPhase', 'ExtropyJar']
    attool = getToolByName(portal, 'archetype_tool')
    for k in trackingtypes:
        attool.setCatalogsByType(k, [config.TOOLNAME, 'portal_catalog'])
    for k in remainingtypes:
        attool.setCatalogsByType(k, [config.TOOLNAME, 'portal_catalog'])

    attool.setCatalogsByType('ExtropyHours', [config.TIMETOOLNAME])
    attool.setCatalogsByType('ExtropyHourGlass', [])

    def setup_indexes(tool):
        for idx_id, idx_type, _ in tool.enumerateIndexes():
            if idx_id in tool.indexes():
                tool.delIndex(idx_id)

            if idx_id == 'SearchableText':
                extra = Extra()
                setattr(extra, 'index_type', 'Okapi BM25 Rank')
                setattr(extra, 'lexicon_id', 'plone_lexicon')
                tool.addIndex(idx_id, idx_type, extra=extra)
            else:
                tool.addIndex(idx_id, idx_type)

        for col_id in tool.enumerateColumns():
            if col_id in tool.schema()[:]:
                tool.delColumn(col_id)
            tool.addColumn(col_id)
        tool.refreshCatalog()

    def add_lexicon(catalog):
        # Lexicon
        catalog._setObject('plone_lexicon', PLexicon('plone_lexicon'))
        lexicon = catalog.plone_lexicon

        pipeline = [
            element_factory.instantiate(
                "Word Splitter", "Unicode Whitespace splitter"),
            element_factory.instantiate(
                "Case Normalizer", "Unicode Case Normalizer"),
        ]
        lexicon._pipeline = tuple(pipeline)

    tool = getToolByName(portal, config.TOOLNAME)
    add_lexicon(tool)
    setup_indexes(tool)

    timetool = getToolByName(portal, config.TIMETOOLNAME)
    add_lexicon(timetool)
    setup_indexes(timetool)


def setupPASRoles(portal, out):
    rmanager = portal.acl_users.portal_role_manager
    for role, title in (
        ('Participant', 'Participant'),
        ('Customer', 'Customer'),
        ('Finance-manager', 'Finance Manager')):
        if role not in rmanager._roles:
            rmanager.addRole(role, title=title)

def importVarious(context):
    """Import various settings.

    Provisional handler that does initialization that is not yet taken
    care of by other handlers.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('extropy_various.txt') is None:
        return

    site = context.getSite()
    out = StringIO()

    tweakTimeTrackerActions(site, out)
    setupCatalogMultiplex(site, out)
    setupPASRoles(site, out)

    logger = context.getLogger('Extropy')
    logger.info(out.getvalue())

def importDependencies(context):
    """Nothing to be done here anymore."""
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('extropy_dependencies.txt') is None:
        return


## XXX: Temporary workaround. This is referenced in the persistent config of
# the import registry. Needs to be removed from there before we can delete this
importPlonePortlets = importDependencies

