from intranett.policy.tests.base import IntranettContentTestCase


class TestDefaultContent(IntranettContentTestCase):

    def test_folders(self):
        site = self.layer['portal']
        ids = site.contentIds()
        self.assertTrue(len(ids) > 3)
