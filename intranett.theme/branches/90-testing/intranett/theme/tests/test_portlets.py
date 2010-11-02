from intranett.policy.tests.base import IntranettTestCase


class TestPortlets(IntranettTestCase):

    def test_navigation_portlet(self):
        portal = self.layer['portal']
        leftcolumn = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(leftcolumn)
        self.assert_(u'navigation' in mapping.keys())
        nav = mapping[u'navigation']
        self.assertEquals(nav.topLevel, 1)
        self.assertEquals(nav.currentFolderOnly, True)
