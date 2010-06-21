from intranett.policy.tests.layer import IntranettLayer

from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five.testbrowser import Browser

# ptc.installProduct("PloneFormGen", quiet=1)

ptc.setupPloneSite(extension_profiles=("intranett.policy:default",))


class IntranettTestCase(ptc.PloneTestCase):
    """ base class for integration tests """

    layer = IntranettLayer


class IntranettFunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    layer = IntranettLayer

    def getCredentials(self):
        return '%s:%s' % (ptc.default_user, ptc.default_password)

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            auth = 'Basic %s' % self.getCredentials()
            browser.addHeader('Authorization', auth)
        return browser
