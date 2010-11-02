from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase


class TestRobots(IntranettFunctionalTestCase):

    def test_disallow(self):
        portal = self.layer['portal']
        browser = get_browser(self.layer, loggedIn=False)
        # We should be allowed to view the page and see the disallow line
        browser.open(portal.absolute_url() + '/robots.txt')
        self.assert_("Disallow: /" in browser.contents)
