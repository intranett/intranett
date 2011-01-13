import unittest2 as unittest

from plone.testing import z2
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from intranett.policy.tests import layer


def get_browser(app, loggedIn=True):
    browser = z2.Browser(app)
    if loggedIn:
        auth = 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD)
        browser.addHeader('Authorization', auth)
    return browser


class IntranettTestCase(unittest.TestCase):

    layer = layer.INTRANETT_INTEGRATION


class IntranettFunctionalTestCase(unittest.TestCase):

    layer = layer.INTRANETT_FUNCTIONAL
