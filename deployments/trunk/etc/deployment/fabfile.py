import os

from fabric.api import cd, env, run, sudo, settings, hide, get

env.shell = "/bin/bash -c"

def touch():
    home = run('pwd')
    run('cd {home} && touch iwashere.txt'.format(home=home))

def svn_info():
    with cd('/srv/jarn'):
        sudo('pwd && svn info', user='jarn')

def dump_db():
    with cd('/srv/jarn'):
        sudo('rm var/snapshotbackups/*', user='jarn')
        sudo('bin/snapshotbackup', user='jarn')

def download_last_dump():
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),
                  warn_only=True):
        existing = sudo('ls -rt1 /srv/jarn/var/snapshotbackups/*', user='jarn')
    for e in existing.split('\n'):
        get(e, os.path.join(os.getcwd(), 'var', 'snapshotbackups'))
