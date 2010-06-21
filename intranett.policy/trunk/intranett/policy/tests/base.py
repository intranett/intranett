from intranett.policy.tests import layer

from Products.PloneTestCase import PloneTestCase as ptc

ptc.installProduct("PloneFormGen", quiet=1)
ptc.setupPloneSite()


class IntranettTestCase(ptc.PloneTestCase):
    """ base class for integration tests """

    layer = layer.intranett


class IntranettFunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    layer = layer.intranett
