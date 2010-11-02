import unittest2 as unittest

from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

from intranett.policy.tests import layer


class MigrateHelper(object):

    layer = None

    @property
    def app(self):
        return self.layer['app']

    @property
    def portal(self):
        return self.layer['portal']

    @property
    def folder(self):
        return self.layer['portal']['test-folder']

    def logout(self):
        from plone.app.testing import logout as lo
        lo()

    def login(self, user=TEST_USER_ID):
        login(self.layer['portal'], user)

    def loginAsPortalOwner(self):
        self.setRoles(['Manager'])

    def setRoles(self, roles):
        from plone.app.testing import setRoles as sr
        sr(self.layer['portal'], TEST_USER_ID, roles)


class IntranettTestCase(unittest.TestCase, MigrateHelper):

    layer = layer.INTRANETT_INTEGRATION


class IntranettFunctionalTestCase(unittest.TestCase, MigrateHelper):

    layer = layer.INTRANETT_FUNCTIONAL

    def getCredentials(self):
        return '%s:%s' % (TEST_USER_ID, TEST_USER_PASSWORD)

    def getBrowser(self, loggedIn=True):
        browser = Browser(self.layer['app'])
        if loggedIn:
            auth = 'Basic %s' % self.getCredentials()
            browser.addHeader('Authorization', auth)
        return browser
