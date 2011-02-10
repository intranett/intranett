from zope.component import queryMultiAdapter
from zope.interface import Interface

from intranett.policy.tests.base import IntranettTestCase


class TestUserPage(IntranettTestCase):

    def _make_one(self, request):
        portal = self.layer['portal']
        return queryMultiAdapter((portal, request), Interface, 'user')

    def test_getitem(self):
        request = self.layer['request']
        view = self._make_one(request)
        user = view['test_user_1_']
        self.failIf(user is None)

    def test_unrestrictedTraverse(self):
        request = self.layer['request']
        view = self._make_one(request)
        user = view.unrestrictedTraverse('test_user_1_', None, False)
        self.failIf(user is None)

    def test_restrictedTraverse(self):
        request = self.layer['request']
        view = self._make_one(request)
        user = view.restrictedTraverse('test_user_1_', None)
        self.failIf(user is None)

    def test_getPhysicalPath(self):
        request = self.layer['request']
        view = self._make_one(request)
        path = view.getPhysicalPath()
        self.assertEqual(path, ('', 'plone', 'user'))
