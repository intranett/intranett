import os

from fabric.api import cd, env, run, sudo, settings, hide, get

env.shell = "/bin/bash -c"
home = '/srv/jarn'

def svn_info():
    with cd(home):
        sudo('pwd && svn info', user='jarn')

def dump_db():
    with cd(home):
        sudo('rm var/snapshotbackups/*', user='jarn')
        sudo('bin/snapshotbackup', user='jarn')

def download_last_dump():
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),
                  warn_only=True):
        existing = sudo('ls -rt1 %s/var/snapshotbackups/*' % home, user='jarn')
    for e in existing.split('\n'):
        get(e, os.path.join(os.getcwd(), 'var', 'snapshotbackups'))

def init_server():
    home = '/home/hannosch'
    with settings(hide('stdout', 'stderr')):
        profile = run('cat %s/.bash_profile' % home)
    profile_lines = profile.split('\n')
    exports = [l for l in profile_lines if l.startswith('export INTRANETT_')]
    if len(exports) < 2:
        # set up environment variables
        start, end = profile_lines[:2], profile_lines[2:]
        subdomain = env.host_string
        domain_line = 'export INTRANETT_DOMAIN=%s.intranett.no\n' % subdomain
        with settings(hide('stdout', 'stderr')):
            front_ip = run('/sbin/ifconfig ethfe | head -n 2 | tail -n 1')
        front_ip = front_ip.lstrip('inet addr:').split()[0]
        front_line = 'export INTRANETT_ZOPE_IP=%s' % front_ip

        new_file = start + [front_line] + [domain_line] + end
        run('cd {home} && echo -e "{content}" > .bash_profile'.format(
            home=home, content='\n'.join(new_file)))
