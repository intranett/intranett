from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase


class TestRejectAnonymous(IntranettFunctionalTestCase):

    def test_loggedin_search(self):
        # Setup
        portal = self.layer['portal']

        browser = get_browser(self.layer['app'], loggedIn=True)
        browser.open(portal.absolute_url() + '/search')
        self.assertEqual(browser.url, portal.absolute_url() + '/search')

    def test_anonymous_search(self):
        # Setup
        portal = self.layer['portal']

        browser = get_browser(self.layer['app'], loggedIn=False)
        browser.open(portal.absolute_url() + '/search')
        self.assertNotEqual(browser.url, portal.absolute_url() + '/search')
        self.assertTrue('require_login' in browser.url)

    def test_anonymous_robotstxt(self):
        # Setup
        portal = self.layer['portal']

        browser = get_browser(self.layer['app'], loggedIn=False)
        browser.open(portal.absolute_url() + '/robots.txt')
        self.assertEqual(browser.url, portal.absolute_url() + '/robots.txt')
