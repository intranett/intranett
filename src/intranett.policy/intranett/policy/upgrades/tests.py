# -*- coding:utf-8 -*-
from zope.component import queryUtility

from intranett.policy.tests.base import IntranettFunctionalTestCase
from intranett.policy.tests.upgrade import UpgradeTests


class TestUpgradeSteps(UpgradeTests, IntranettFunctionalTestCase):

    def after_46(self):
        # tested by GS export diff
        pass

    def after_47(self):
        from jarn.xmpp.core.interfaces import IXMPPPasswordStorage
        pw_storage = queryUtility(IXMPPPasswordStorage)
        self.assertTrue(pw_storage is not None)
