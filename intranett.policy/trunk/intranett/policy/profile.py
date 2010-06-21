from zope.interface import implements

from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonQ


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'borg.localrole:default',
            u'plone.app.iterate:plone.app.iterate',
            u'plone.app.openid:default',
            u'plonetheme.classic:default',
            u'plonetheme.sunburst:default',
            u'Products.PloneFormGen:default',
            u'Products.PloneFormGen:typeoverrides25x',
            ]

class HiddenProducts(object):
    implements(INonQ)

    def getNonInstallableProducts(self):
        return [
            'kupu',
            'plone.app.iterate',
            'plone.app.openid',
            'plonetheme.classic',
            'Products.CMFPlacefulWorkflow',
            'Products.kupu',
            'Products.Marshall',
            'Products.PloneFormGen',
        ]
