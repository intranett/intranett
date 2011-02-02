from zope.interface import implements

from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonQ


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'borg.localrole:default',
            u'collective.ATClamAV:default',
            u'collective.flag:default',
            u'plone.app.caching:default',
            u'plone.app.discussion:default',
            u'plone.app.iterate:plone.app.iterate',
            u'plone.app.openid:default',
            u'plone.app.registry:default',
            u'plone.app.z3cform:default',
            u'plonetheme.classic:default',
            u'plonetheme.sunburst:default',
            u'Products.PloneFormGen:default',
            u'Products.PloneFormGen:typeoverrides25x',
            u'intranett.theme:default',
            ]

class HiddenProducts(object):
    implements(INonQ)

    def getNonInstallableProducts(self):
        return [
            'collective.ATClamAV',
            'collective.flag',
            'kupu',
            'plone.app.caching',
            'plone.app.discussion',
            'plone.app.iterate',
            'plone.app.openid',
            'plone.app.registry',
            'plone.app.z3cform',
            'plonetheme.classic',
            'Products.CMFPlacefulWorkflow',
            'Products.kupu',
            'Products.Marshall',
            'Products.PloneFormGen',
            'intranett.theme',
        ]
