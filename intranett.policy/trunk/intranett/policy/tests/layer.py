from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc


class IntranettLayer(BasePTCLayer):
    """ layer for integration tests """

    def afterSetUp(self):
        import intranett.policy

        fiveconfigure.debug_mode = True
        zcml.load_config("meta.zcml", intranett.policy)
        zcml.load_config("configure.zcml", intranett.policy)
        zcml.load_config("overrides.zcml", intranett.policy)
        fiveconfigure.debug_mode = False
        ztc.installPackage("intranett.policy", quiet=True)
        self.addProfile('plone.app.imaging:default')

    def beforeTearDown(self):
        pass


intranett = IntranettLayer(bases=[ptc_layer])
