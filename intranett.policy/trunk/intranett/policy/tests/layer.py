from Products.PloneTestCase import layer
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc


class IntranettLayer(layer.PloneSite):

    @classmethod
    def setUp(cls):
        import intranett.policy

        fiveconfigure.debug_mode = True
        zcml.load_config("meta.zcml", intranett.policy)
        zcml.load_config("configure.zcml", intranett.policy)
        zcml.load_config("overrides.zcml", intranett.policy)
        fiveconfigure.debug_mode = False
        ztc.installPackage("intranett.policy", quiet=1)

    @classmethod
    def tearDown(cls):
        pass
