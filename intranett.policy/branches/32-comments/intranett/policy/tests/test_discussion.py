from plone.app.discussion.interfaces import IDiscussionSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility

from intranett.policy.tests.base import IntranettTestCase


class TestSiteSetup(IntranettTestCase):

    def test_moderate_action_invisible(self):
        user = getToolByName(self.portal, 'portal_actions').user
        comments = [a for a in user.listActions() if a.id == 'review-comments']
        self.assertEquals(len(comments), 1)
        self.assertEquals(comments[0].visible, False)

    def test_registry_defaults(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings)
        self.assertEquals(settings.anonymous_comments, False)
        self.assertEquals(settings.captcha, 'disabled')
        self.assertEquals(settings.globally_enabled, False)
        self.assertEquals(settings.show_commenter_image, True)
        self.assertEquals(settings.text_transform, 'text/x-web-intelligent')
