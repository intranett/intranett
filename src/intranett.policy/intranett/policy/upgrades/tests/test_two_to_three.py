from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.upgrades.two import two_to_three


class TestFunctionalMigrations(IntranettTestCase):

    def test_two_to_three(self):
        portal = self.layer['portal']
        existing_roles = set(getattr(portal, '__ac_roles__', []))
        existing_roles.remove('Site Administrator')
        portal.__ac_roles__ = tuple(existing_roles)

        pstool = getToolByName(portal, 'portal_setup')
        two_to_three(pstool)
        existing_roles = set(getattr(portal, '__ac_roles__', []))
        self.assertTrue('Site Administrator' in existing_roles)
