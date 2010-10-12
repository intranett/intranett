from unittest import TestSuite
import doctest
from Testing.ZopeTestCase import ZopeDocFileSuite
from intranett.policy.tests.base import IntranettFunctionalTestCase


optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = TestSuite([
        ZopeDocFileSuite(
            'tests/frontpage.txt', package='intranett.theme',
            test_class=IntranettFunctionalTestCase,
            optionflags=optionflags)])
    return suite
