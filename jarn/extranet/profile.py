from zope.interface import implements

from Products.CMFPlone.interfaces import INonInstallable


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'jarn.extranet.customer:default',
            u'plone.app.blob:default',
            u'plone.app.blob:atfile-replacement',
            u'plone.app.imaging:default',
            u'plone.app.z3cform:default',
            u'collective.dancing:default',
            u'collective.indexing:default',
            u'membrane:default',
            u'membrane:examples',
            u'Products.LinguaPlone:LinguaPlone',
            u'Products.CacheSetup:default',
            u'Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow',
            u'Products.ImageRepository:default',
            u'Products.RedirectionTool:default',
            u'Products.RichImage:default',
            u'Products.ATVocabularyManager:default',
            u'Maps:default',
            u'Products.NuPlone:nuplone',
            u'plone.app.openid:default',
            u'borg.localrole:default',
            u'plone.app.iterate:plone.app.iterate',
            u'archetypes.referencebrowserwidget:default',
            u'collective.portlet.content:default',
            ]
