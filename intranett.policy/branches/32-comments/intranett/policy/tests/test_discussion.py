from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase


class TestSiteSetup(IntranettTestCase):

    def test_moderate_action_invisible(self):
        user = getToolByName(self.portal, 'portal_actions').user
        comments = [a for a in user.listActions() if a.id == 'review-comments']
        self.assertEquals(len(comments), 1)
        self.assertEquals(comments[0].visible, False)
