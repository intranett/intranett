from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Extropy import config


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
    """We manually hook up the dependencies installers."""
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('extropy_dependencies.txt') is None:
        return

    out = StringIO()
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')
    products = [
        'Memo',
        'Invoice',
    ]
    for product in products:
        if not qi.isProductInstalled(product):
            qi.installProducts([product])

    if not qi.isProductInstalled('Extropy'):
        qi.notifyInstalled('Extropy')

    logger = context.getLogger('Extropy')
    logger.info(out.getvalue())

## XXX: Temporary workaround. This is referenced in the persistent config of
# the import registry. Needs to be removed from there before we can delete this
importPlonePortlets = importDependencies

