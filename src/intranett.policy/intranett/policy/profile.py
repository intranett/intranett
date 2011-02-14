from zope.interface import implements

from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonQ


HIDDEN = ['collective.ATClamAV', 'plone.app.caching',
    'plone.app.discussion', 'plone.app.openid', 'plone.app.registry',
    'plone.app.z3cform', 'plone.formwidget.autocomplete', 'plonetheme.classic',
    'Products.PloneFormGen', 'intranett.theme']


class HiddenProducts(object):
    implements(INonQ)

    def getNonInstallableProducts(self):
        return HIDDEN + [
            'kupu',
            'plone.app.iterate',
            'Products.CMFPlacefulWorkflow',
            'Products.kupu',
            'Products.Marshall',
        ]


def register_profile(name='default'):
    from Products.GenericSetup.interfaces import EXTENSION
    from Products.GenericSetup.registry import _profile_registry
    product = __package__
    title = '%s:%s' % (product, name)
    _profile_registry.registerProfile(name, title, description=u'',
        path='profiles/%s' % name, product=product, profile_type=EXTENSION)


IMPORT_STEPS = {}


def import_step(depends=('toolset', 'types', 'workflow')):

    def decorator(fun):
        name = fun.__module__ + fun.__name__
        IMPORT_STEPS[name] = (fun, depends)
        return fun
    return decorator


def register_import_steps():
    from Products.GenericSetup.registry import _import_step_registry
    from Products.GenericSetup.zcml import _import_step_regs
    for name, info in IMPORT_STEPS.items():
        _import_step_regs.append(name)
        _import_step_registry.registerStep(name, handler=info[0],
            dependencies=info[1], title=name)
