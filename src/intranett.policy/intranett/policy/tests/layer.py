from zope.configuration import xmlconfig
from plone.testing import z2
from plone.app.testing import PloneFixture
from plone.app.testing import PloneTestLifecycle
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class IntranettFixture(PloneFixture):

    # No sunburst please
    extensionProfiles = ()

INTRANETT_FIXTURE = IntranettFixture()


class IntranettTestLifecycle(PloneTestLifecycle):

    defaultBases = (INTRANETT_FIXTURE, )


class IntegrationTesting(IntranettTestLifecycle, z2.IntegrationTesting):
    pass


class FunctionalTesting(IntranettTestLifecycle, z2.FunctionalTesting):
    pass


class IntranettLayer(PloneSandboxLayer):
    """ layer for integration tests """

    defaultBases = (INTRANETT_FIXTURE, )

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


INTRANETT_LAYER = IntranettLayer()
INTRANETT_INTEGRATION = IntegrationTesting(
    bases=(INTRANETT_LAYER, ), name="Intranett:Integration")
INTRANETT_FUNCTIONAL = FunctionalTesting(
    bases=(INTRANETT_LAYER, ), name="Intranett:Functional")


class IntranettContentLayer(PloneSandboxLayer):
    """ layer for default content tests """

    defaultBases = (INTRANETT_LAYER, )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'intranett.policy:content')

INTRANETT_CONTENT_LAYER = IntranettContentLayer()
INTRANETT_CONTENT_INTEGRATION = IntegrationTesting(
    bases=(INTRANETT_CONTENT_LAYER, ), name="IntranettContent:Integration")
