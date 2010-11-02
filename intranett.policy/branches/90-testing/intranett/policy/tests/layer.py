from plone.app.testing import applyProfile
from plone.app.testing import PloneFixture
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.layers import PloneTestLifecycle
from plone.testing import z2
from zope.configuration import xmlconfig


class NightPloneFixture(PloneFixture):

    # No sunburst please
    extensionProfiles = ()

NIGHT_PLONE_FIXTURE = NightPloneFixture()


class NightPloneTestLifecycle(PloneTestLifecycle):

    defaultBases = (NIGHT_PLONE_FIXTURE, )


class IntegrationTesting(NightPloneTestLifecycle, z2.IntegrationTesting):
    pass


class FunctionalTesting(NightPloneTestLifecycle, z2.FunctionalTesting):
    pass


class IntranettLayer(PloneSandboxLayer):
    """ layer for integration tests """

    defaultBases = (NIGHT_PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import intranett.policy

        xmlconfig.file("meta.zcml", intranett.policy,
                       context=configurationContext)
        xmlconfig.file("configure.zcml", intranett.policy,
                       context=configurationContext)
        xmlconfig.file("overrides.zcml", intranett.policy,
                       context=configurationContext)

        z2.installProduct(app, 'Products.PloneFormGen')
        z2.installProduct(app, 'intranett.theme')
        z2.installProduct(app, 'intranett.policy')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'intranett.policy')
        z2.uninstallProduct(app, 'intranett.theme')
        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'intranett.policy:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Folder', 'test-folder')
        setRoles(portal, TEST_USER_ID, ['Member'])


INTRANETT_FIXTURE = IntranettLayer()

INTRANETT_INTEGRATION = IntegrationTesting(bases=(INTRANETT_FIXTURE, ),
                                           name="intranett:Integration")
INTRANETT_FUNCTIONAL = FunctionalTesting(bases=(INTRANETT_FIXTURE, ),
                                         name="intranett:Functional")
