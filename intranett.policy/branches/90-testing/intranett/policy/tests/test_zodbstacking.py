import unittest2 as unittest
from plone.testing import z2
from plone.app.testing import layers
from plone.app.testing import helpers
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


def storagestack(storage):
    stack = []
    stack.append(storage.getName())
    while hasattr(storage, 'base'):
        storage = storage.base
        try:
            stack.append(storage.getName())
        except AttributeError:
            pass
    return stack


def printzodb(self):
    """Docstring"""
    return repr(self._p_jar._db)


def printstoragestack(self):
    """Docstring"""
    return repr(storagestack(self._p_jar._db._storage))


from OFS.Application import Application
Application.printzodb = printzodb
Application.printstoragestack = printstoragestack


class ZODBStackingTests(unittest.TestCase):

    layer = z2.STARTUP
    expectedstack = ['Startup', 'MappingStorage']

    def test_zodbApplicationObject(self):
        conn = self.layer['zodbDB'].open()
        try:
            self.failUnless('Application' in conn.root())
        finally:
            conn.close()

    def test_zodbStorageStack(self):
        self.assertEqual(storagestack(self.layer['zodbDB']._storage), self.expectedstack)

    def test_zopeAppZodb(self):
        with z2.zopeApp() as app:
            self.assertEqual(app._p_jar._db, self.layer['zodbDB'])

    def test_zopeAppStorageStack(self):
        with z2.zopeApp() as app:
            self.assertEqual(storagestack(app._p_jar._db._storage), self.expectedstack)


class IntegrationTests(ZODBStackingTests):

    layer = z2.INTEGRATION_TESTING
    expectedstack = ['Startup', 'MappingStorage']

    def test_layerAppZodb(self):
        self.assertEqual(self.layer['app']._p_jar._db, self.layer['zodbDB'])

    def test_layerAppStorageStack(self):
        self.assertEqual(storagestack(self.layer['app']._p_jar._db._storage), self.expectedstack)


class FunctionalTests(IntegrationTests):

    layer = z2.FUNCTIONAL_TESTING
    expectedstack = ['FunctionalTest', 'Startup', 'MappingStorage']

    def test_browserAppZodb(self):
        browser = z2.Browser(self.layer['app'])
        browser.open('http://localhost/printzodb')
        self.assertEqual(browser.contents, repr(self.layer['zodbDB']))

    def test_browserAppStorageStack(self):
        browser = z2.Browser(self.layer['app'])
        browser.open('http://localhost/printstoragestack')
        self.assertEqual(browser.contents, repr(self.expectedstack))


#
# Plone layer
#

class PloneZODBStackingTests(ZODBStackingTests):

    layer = layers.PLONE_FIXTURE
    expectedstack = ['PloneFixture', 'Startup', 'MappingStorage']


class PloneIntegrationTests(IntegrationTests):

    layer = layers.PLONE_INTEGRATION_TESTING
    expectedstack = ['PloneFixture', 'Startup', 'MappingStorage']


class PloneFunctionalTests(FunctionalTests):

    layer = layers.PLONE_FUNCTIONAL_TESTING
    expectedstack = ['FunctionalTest', 'PloneFixture', 'Startup', 'MappingStorage']


#
# Custom layer
#

class CustomLayer(helpers.PloneSandboxLayer):
    pass


CUSTOM_LAYER = CustomLayer()
CUSTOM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CUSTOM_LAYER,), name='CustomLayer:Integration')
CUSTOM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CUSTOM_LAYER,), name='CustomLayer:Functional')


class CustomZODBStackingTests(ZODBStackingTests):

    layer = CUSTOM_LAYER
    expectedstack = ['CustomLayer', 'PloneFixture', 'Startup', 'MappingStorage']


class CustomIntegrationTests(IntegrationTests):

    layer = CUSTOM_INTEGRATION_TESTING
    expectedstack = ['CustomLayer', 'PloneFixture', 'Startup', 'MappingStorage']


class CustomFunctionalTests(FunctionalTests):

    layer = CUSTOM_FUNCTIONAL_TESTING
    expectedstack = ['FunctionalTest', 'CustomLayer', 'PloneFixture', 'Startup', 'MappingStorage']


#
# Custom fixture, lifecycle, and layer
#

class CustomPloneFixture(layers.PloneFixture):
    extensionProfiles = ()

CUSTOM_PLONE_FIXTURE = CustomPloneFixture()


class CustomPloneTestLifecycle(layers.PloneTestLifecycle):
    defaultBases = (CUSTOM_PLONE_FIXTURE,)


class CustomIntegrationTesting(CustomPloneTestLifecycle, z2.IntegrationTesting):
    pass

class CustomFunctionalTesting(CustomPloneTestLifecycle, z2.FunctionalTesting):
    pass


class CustomPloneLayer(helpers.PloneSandboxLayer):
    defaultBases = (CUSTOM_PLONE_FIXTURE,)


CUSTOM_PLONE_LAYER = CustomPloneLayer()
CUSTOM_PLONE_INTEGRATION_TESTING = CustomIntegrationTesting(
    bases=(CUSTOM_PLONE_LAYER,), name='CustomPloneLayer:Integration')
CUSTOM_PLONE_FUNCTIONAL_TESTING = CustomFunctionalTesting(
    bases=(CUSTOM_PLONE_LAYER,), name='CustomPloneLayer:Functional')


class CustomPloneZODBStackingTests(ZODBStackingTests):

    layer = CUSTOM_PLONE_LAYER
    expectedstack = ['CustomPloneLayer', 'PloneFixture', 'Startup', 'MappingStorage']


class CustomPloneIntegrationTests(IntegrationTests):

    layer = CUSTOM_PLONE_INTEGRATION_TESTING
    expectedstack = ['CustomPloneLayer', 'PloneFixture', 'Startup', 'MappingStorage']


class CustomPloneFunctionalTests(FunctionalTests):

    layer = CUSTOM_PLONE_FUNCTIONAL_TESTING
    expectedstack = ['FunctionalTest', 'CustomPloneLayer', 'PloneFixture', 'Startup', 'MappingStorage']
