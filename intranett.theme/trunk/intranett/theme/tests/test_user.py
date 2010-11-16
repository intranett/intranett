from zope.component import queryMultiAdapter
from zope.interface import Interface

from intranett.policy.tests.base import IntranettTestCase


class TestUserPage(IntranettTestCase):

    def _make_one(self):
        return queryMultiAdapter((self.portal, self.portal.REQUEST),
            Interface, 'user')

    def test_no_username(self):
        view = self._make_one()
        self.assertEquals(view.username(), '')
        self.assertEquals(len(view.user_content()), 0)

    def test_with_username(self):
        request = self.portal.REQUEST
        request.form['name'] = 'no_user'
        view = self._make_one()
        self.assertEquals(view.username(), 'no_user')
        self.assertEquals(len(view.user_content()), 0)
