from plone.app.testing import applyProfile
from plone.app.testing import PloneFixture
from plone.app.testing import PloneTestLifecycle
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from zope.configuration import xmlconfig


class NightPloneFixture(PloneFixture):

    # No sunburst please
    extensionProfiles = ()

    def setUpZCML(self):
        super(NightPloneFixture, self).setUpZCML()

        # Work around z3c.unconfigure not doing its job in test setups
        from zope.component import getGlobalSiteManager
        from plone.app.workflow.interfaces import ISharingPageRole
        sm = getGlobalSiteManager()
        sm.unregisterUtility(provided=ISharingPageRole, name=u'Reviewer')


NIGHT_PLONE_FIXTURE = NightPloneFixture()


class NightPloneTestLifecycle(PloneTestLifecycle):

    defaultBases = (NIGHT_PLONE_FIXTURE, )

    def testSetUp(self):
        super(NightPloneTestLifecycle, self).testSetUp()

        # Make sure browser tests use the topmost db
        import Zope2
        self['_stuff'] = Zope2.bobo_application._stuff
        Zope2.bobo_application._stuff = (self['zodbDB'],) + self['_stuff'][1:]

    def testTearDown(self):
        super(NightPloneTestLifecycle, self).testTearDown()

        # Cleanup global variables
        import Zope2
        Zope2.bobo_application._stuff = self['_stuff']
        del self['_stuff']


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
