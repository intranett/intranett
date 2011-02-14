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
