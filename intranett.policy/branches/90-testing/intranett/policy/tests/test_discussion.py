from plone.app.discussion.interfaces import IDiscussionSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility

from intranett.policy.tests.base import IntranettTestCase


class TestCommenting(IntranettTestCase):

    def test_moderate_action_invisible(self):
        portal = self.layer['portal']
        user = getToolByName(portal, 'portal_actions').user
        comments = [a for a in user.listActions() if a.id == 'review-comments']
        self.assertEquals(len(comments), 1)
        self.assertEquals(comments[0].visible, False)

    def test_registry_defaults(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings)
        self.assertEquals(settings.anonymous_comments, False)
        self.assertEquals(settings.captcha, 'disabled')
        self.assertEquals(settings.globally_enabled, True)
        self.assertEquals(settings.show_commenter_image, True)
        self.assertEquals(settings.text_transform, 'text/x-web-intelligent')

    def test_types_enabled(self):
        portal = self.layer['portal']
        tt = getToolByName(portal, 'portal_types')
        self.assertEquals(tt['Document'].allow_discussion, True)
        self.assertEquals(tt['Event'].allow_discussion, True)
        self.assertEquals(tt['News Item'].allow_discussion, True)

    def test_types_disabled(self):
        portal = self.layer['portal']
        tt = getToolByName(portal, 'portal_types')
        self.assertEquals(tt['Folder'].allow_discussion, False)
        self.assertEquals(tt['Link'].allow_discussion, False)
        self.assertEquals(tt['Topic'].allow_discussion, False)
