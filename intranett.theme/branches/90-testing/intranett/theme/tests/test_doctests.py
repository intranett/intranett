import doctest
from doctest import DocFileSuite
from unittest import TestSuite

from plone.testing import layered
from intranett.policy.tests.layer import INTRANETT_FUNCTIONAL

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = TestSuite()
    suite.addTests([
        layered(DocFileSuite('employeelisting.txt',
                             package='intranett.theme.tests'),
                layer=INTRANETT_FUNCTIONAL),
    ])
    return suite
