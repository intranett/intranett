from Products.PloneTestCase import ptc

from intranett.policy.tests import layer

ptc.installProduct("PloneFormGen", quiet=1)
ptc.setupPloneSite()


class IntranettTestCase(ptc.PloneTestCase):
    """ base class for integration tests """

    layer = layer.intranett


class IntranettFunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    layer = layer.intranett
