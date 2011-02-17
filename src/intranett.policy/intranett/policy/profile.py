from zope.interface import implements

from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonQ


HIDDEN = ['collective.flag', 'collective.ATClamAV', 'plone.app.caching',
    'plone.app.discussion', 'plone.app.openid', 'plone.app.registry',
    'plone.app.z3cform', 'plonetheme.classic', 'Products.PloneFormGen',
    'intranett.theme']


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [u'%s:default' % h for h in HIDDEN] + [
            u'borg.localrole:default',
            u'plone.app.iterate:plone.app.iterate',
            u'plonetheme.sunburst:default',
            u'Products.PloneFormGen:typeoverrides25x',
            ]

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
