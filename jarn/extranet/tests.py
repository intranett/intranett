import unittest

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase as ztc
ptc.setupPloneSite()

import jarn.extranet

class ExtranetLayer(PloneSite):
    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml',
                         jarn.extranet)
        fiveconfigure.debug_mode = False
        ztc.installPackage('jarn.extranet')

    @classmethod
    def tearDown(cls):
        pass


class TestCase(ptc.PloneTestCase):

    layer = ExtranetLayer


def test_suite():
    return unittest.TestSuite([

        ])
