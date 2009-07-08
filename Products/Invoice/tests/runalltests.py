#
# Runs all tests in the current directory [and below]
#
# Execute like:
#   python runalltests.py [-R]
#

__version__ = '0.3.0'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
TestRunner = unittest.TextTestRunner
suite = unittest.TestSuite()

def test_finder(recurse, dir, names):
    if dir == os.curdir or '__init__.py' in names:
        parts = [x for x in dir[len(os.curdir):].split(os.sep) if x]
        tests = [x for x in names if x.startswith('test') and x.endswith('.py')]
        for test in tests:
            modpath = parts + [test[:-3]]
            m = __import__('.'.join(modpath))
            for part in modpath[1:]:
                m = getattr(m, part)
            if hasattr(m, 'test_suite'):
                suite.addTest(m.test_suite())
    if not recurse:
        names[:] = []

if __name__ == '__main__':
    os.path.walk(os.curdir, test_finder, '-R' in sys.argv)
    TestRunner().run(suite)

