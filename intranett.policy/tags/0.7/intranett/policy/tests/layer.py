from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc


class IntranettLayer(BasePTCLayer):
    """ layer for integration tests """

    def afterSetUp(self):
        self.removeContent()

        import intranett.policy
        fiveconfigure.debug_mode = True
        zcml.load_config("meta.zcml", intranett.policy)
        zcml.load_config("configure.zcml", intranett.policy)
        zcml.load_config("overrides.zcml", intranett.policy)
        fiveconfigure.debug_mode = False
        ztc.installPackage("intranett.policy", quiet=True)
        ztc.installPackage("intranett.theme", quiet=True)
        self.addProfile('intranett.policy:default')

    def removeContent(self):
        id_ = 'front-page'
        if id_ in self.portal:
            self.loginAsPortalOwner()
            self.portal.setDefaultPage(None)
            del self.portal[id_]
        # We don't remove the Members/test_user_1_ folder, as it is too
        # convenient to use in tests
        for id_ in ('news', 'events'):
            if id_ in self.portal:
                del self.portal[id_]
        # The helpful testing machinery installs sunburst for us :(
        skins = self.portal.portal_skins
        for s in list(skins.keys()):
            if s.startswith('sunburst'):
                del skins[s]
        del skins.selections['Sunburst Theme']
        # TODO, there's also an actions.xml


intranett = IntranettLayer(bases=[ptc_layer])
