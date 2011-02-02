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

    def setUpZCML(self):
        super(IntranettFixture, self).setUpZCML()

        # Work around z3c.unconfigure not doing its job in test setups
        from zope.component import getGlobalSiteManager
        from plone.app.workflow.interfaces import ISharingPageRole
        sm = getGlobalSiteManager()
        sm.unregisterUtility(provided=ISharingPageRole, name=u'Reviewer')

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
        import iw.rejectanonymous

        xmlconfig.file("meta.zcml", intranett.policy,
                       context=configurationContext)
        xmlconfig.file("configure.zcml", intranett.policy,
                       context=configurationContext)
        xmlconfig.file("overrides.zcml", intranett.policy,
                       context=configurationContext)

        # Need to explicitly load this because z3c.autoinclude is not run
        xmlconfig.file('configure.zcml', iw.rejectanonymous,
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
    bases=(INTRANETT_LAYER, ), name="IntranettLayer:Integration")
INTRANETT_FUNCTIONAL = FunctionalTesting(
    bases=(INTRANETT_LAYER, ), name="IntranettLayer:Functional")
