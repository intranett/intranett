from zope.interface import implements

from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonQ


HIDDEN = ['collective.ATClamAV', 'plone.app.caching',
    'plone.app.discussion', 'plone.app.openid', 'plone.app.registry',
    'plone.app.z3cform', 'plone.formwidget.autocomplete', 'plone.session',
    'plonetheme.classic', 'Products.PloneFormGen', 'intranett.theme']


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
