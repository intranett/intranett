import unittest2 as unittest

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

from intranett.policy.tests import layer


def get_browser(layer, loggedIn=True):
    browser = Browser(layer['app'])
    if loggedIn:
        auth = 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD)
        browser.addHeader('Authorization', auth)
    return browser


class IntranettTestCase(unittest.TestCase):

    layer = layer.INTRANETT_INTEGRATION


class IntranettFunctionalTestCase(unittest.TestCase):

    layer = layer.INTRANETT_FUNCTIONAL
