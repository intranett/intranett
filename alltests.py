"""
This script assumes to be called via python alltests.py while the current
directory is the buildout root.

The script will start the local ejabberd. As part of the test layer setup,
the ejabberd database will be reset. Since dev.intranett.no and the Jenkins
slave run on the same machine, this means the dev.intranett.no site will also
get its ejabberd database reset frequently.
"""

import os
import sys


def main(args=[]):
    curdir = os.curdir
    conf = os.path.join(curdir, 'etc', 'supervisord-test.conf')
    test = os.path.join(curdir, 'bin', 'coverage')
    supervisord = os.path.join(curdir, 'bin', 'supervisord')
    supervisorctl = os.path.join(curdir, 'bin', 'supervisorctl')
    arg = ' '.join(args)

    value = 0
    try:
        if os.path.exists(supervisord):
            print '#### Starting supervisor ####'
            _ = os.system('%s -c %s' % (supervisord, conf))

        print '#### Running tests ####'
        value = os.system('%s %s' % (test, arg))
        print '#### Finished tests ####'
    finally:
        if os.path.exists(supervisorctl):
            print '#### Stopping supervisor ####'
            _ = os.system('%s -c %s shutdown' % (supervisorctl, conf))

    return value


if __name__ == '__main__':
    args = sys.argv[1:]
    result = main(args)
    sys.exit(result)
