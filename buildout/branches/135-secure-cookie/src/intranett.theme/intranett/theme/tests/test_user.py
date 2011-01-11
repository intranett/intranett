from zope.component import queryMultiAdapter
from zope.interface import Interface

from intranett.policy.tests.base import IntranettTestCase


class TestUserPage(IntranettTestCase):

    def _make_one(self, request):
        portal = self.layer['portal']
        return queryMultiAdapter((portal, request), Interface, 'user')

    def test_no_username(self):
        request = self.layer['request']
        view = self._make_one(request)
        self.assertEquals(view.username(), '')
        self.assertEquals(len(view.user_content()), 0)

    def test_with_username(self):
        request = self.layer['request']
        request.form['name'] = 'no_user'
        view = self._make_one(request)
        self.assertEquals(view.username(), 'no_user')
        self.assertEquals(len(view.user_content()), 0)
