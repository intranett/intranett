import sys
import os
import os.path
import time
from ConfigParser import ConfigParser
from datetime import datetime

from fabric.api import cd
from fabric.api import env
from fabric.api import get
from fabric.api import put
from fabric.api import hide
from fabric.api import local
from fabric.api import run
from fabric.api import settings
from fabric.api import show
import pkg_resources

env.shell = "/bin/bash -c"
_staging = ['dev', 'demo']
env.roledefs['staging'] = _staging
_production = set(env.servers.keys()) - set(_staging)
env.roledefs['production'] = list(_production)

BUILDOUT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
LIVEBACKUPS = os.path.join(BUILDOUT_ROOT, 'var', 'livebackups')

CRON_MAILTO = 'hosting@jarn.com'
DISTRIBUTE_VERSION = '0.6.14'
HOME = '/srv/jarn'
VENV = '/srv/jarn'
PIL_VERSION = '1.1.7-jarn1'
PIL_LOCATION = 'http://dist.jarn.com/public/PIL-%s.zip' % PIL_VERSION


def version_info():
    with cd(VENV):
        with settings(hide('running')):
            run('git log -n 2 --pretty="%h %ci%n%s%n"')


def restore_db():
    with cd(VENV):
        existing = run('ls -rt1 %s/var/snapshotbackups/*' % VENV)
        if len(existing.split('\n')) != 3:
            print("There are not excactly 3 files in the snapshotbackups "
                  "directory, please investigate")
            sys.exit(1)
        run('bin/supervisorctl stop varnish')
        run('bin/supervisorctl stop zope:*')
        run('bin/supervisorctl stop zeo')
        run('bin/snapshotrestore')
        with settings(hide('warnings'), warn_only=True):
            run('rm -r var/blobstorage/*')
        run('tar xzf var/snapshotbackups/*-blobstorage.tgz')
        run('bin/supervisorctl start zeo')
        run('bin/supervisorctl start zope:instance1')
        run('bin/supervisorctl start zope:instance2')
        time.sleep(30)
        run('bin/supervisorctl start varnish')


def dump_db():
    with cd(VENV):
        # We should cleanup some old snapshots after a while
        # with settings(hide('warnings'), warn_only=True):
        #     run('rm var/snapshotbackups/*')
        run('bin/snapshotbackup')
        run('tar czf var/snapshotbackups/%s-blobstorage.tgz var/blobstorage' %
            (datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")))


def download_last_dump():
    localdir = os.path.join(LIVEBACKUPS, env.host_string)
    snapshotdir = os.path.join(BUILDOUT_ROOT, 'var', 'snapshotbackups')
    with settings(hide('warnings'), warn_only=True):
        if not os.path.exists(localdir):
            os.makedirs(localdir)
        local('rm %s/*' % localdir)
        # If the snapshotdir is a file (which it should not be) or a symlink
        # we delete it and create a new symlink to the latest download.
        try:
            os.remove(snapshotdir)
        except OSError:
            print("%s is not a symlink, not removing" % snapshotdir)
        try:
            os.symlink(localdir, snapshotdir)
        except OSError:
            print("%s already exists, can't create symlink to %s" %
                (snapshotdir, localdir))

    with settings(hide('warnings', 'running', 'stdout', 'stderr'),
                  warn_only=True):
        existing = run('ls -rt1 %s/var/snapshotbackups/*' % VENV)
    for e in existing.split('\n'):
        get(e, localdir)


def upload_last_dump():
    localdir = os.path.join(LIVEBACKUPS, env.host_string)
    existing = local('ls -rt1 %s/*' % localdir)
    if len(existing.split('\n')) != 3:
        print("There are not excactly 3 files in the local snapshotbackups "
              "directory, please investigate")
        sys.exit(1)
    with cd(VENV):
        with settings(hide('warnings'), warn_only=True):
            run('rm var/snapshotbackups/*')
        put("%s/*" % localdir, "var/snapshotbackups/")


def reload_nginx():
    run('sudo /etc/init.d/nginx reload')


def update():
    _prepare_update(newest=False)
    with cd(VENV):
        run('bin/supervisorctl stop varnish')
        run('bin/supervisorctl stop zope:*')
        run('bin/instance-debug upgrade')
        run('bin/supervisorctl start zope:instance1')
        run('bin/supervisorctl start zope:instance2')
        time.sleep(30)
        run('bin/supervisorctl start varnish')


def full_update():
    _prepare_update()
    with cd(VENV):
        run('bin/supervisorctl shutdown')
        time.sleep(5)
        run('bin/supervisord')
        run('bin/supervisorctl stop varnish')
        run('bin/supervisorctl stop zope:*')
        run('bin/instance-debug upgrade')
        run('bin/supervisorctl start zope:instance1')
        run('bin/supervisorctl start zope:instance2')
        time.sleep(30)
        run('bin/supervisorctl start varnish')


def init_server():
    envvars = _set_environment_vars()
    _set_cron_mailto()
    _disable_svn_store_passwords()
    _setup_ssh_keys()
    _add_nginx_include()
    _virtualenv()

    # switch / clone git
    is_git = _is_git_repository()
    _git_update(is_git=is_git)
    _buildout(envvars=envvars)
    initial = not is_git
    _create_plone_site(initial=initial)
    # reload nginx so we pick up the new local/jarn.conf file and the buildout
    # local nginx-sites one
    reload_nginx()
    with cd(VENV):
        run('bin/supervisord')


def reset_server():
    _prepare_update()
    with cd(VENV):
        run('bin/supervisorctl shutdown')
        time.sleep(5)
        run('rm var/filestorage/D*')
        with settings(hide('warnings'), warn_only=True):
            run('rm -r var/blobstorage/*')
    _create_plone_site(initial=True)
    reload_nginx()
    with cd(VENV):
        run('bin/supervisord')


def _add_nginx_include():
    with cd('/etc/nginx/local'):
        text = 'include /srv/jarn/nginx-sites/*.conf;\n'
        run('echo -e "{text}" > jarn.conf'.format(text=text))
        run('chmod 664 jarn.conf')


def _buildout(envvars, newest=True):
    domain = envvars['domain']
    front = envvars['front']
    arg = '' if newest else '-N'
    with cd(VENV):
        run('bin/python2.6 bootstrap.py -dc production.cfg')
        with settings(hide('stdout', 'stderr', 'warnings'), warn_only=True):
            run('mkdir downloads')
        run('{x1}; {x2}; bin/buildout -c production.cfg -t 5 {arg}'.format(
            x1=front, x2=domain, arg=arg))
        run('chmod 700 var/blobstorage')


def _create_plone_site(initial=False):
    title = env.server.config.get('title', '%s intranett' % env.host_string)
    language = env.server.config.get('language', 'no')
    with cd(VENV):
        with settings(hide('warnings'), warn_only=True):
            if initial:
                run('bin/zeo start')
                time.sleep(3)
            cfg = os.path.join(BUILDOUT_ROOT, 'cfgs', 'credentials.cfg')
            config = ConfigParser()
            config.read(cfg)
            value = config.get('credentials', 'zope-user')
            password = value.split(':')[-1]
            run('bin/instance-debug create_site --title="%s" --language=%s '
                '--rootpassword=%s' % (title, language, password))
            if initial:
                run('bin/zeo stop')


def _disable_svn_store_passwords():
    svn_config = os.path.join(HOME, '.subversion', 'config')
    with settings(hide('stdout', 'stderr', 'warnings'), warn_only=True):
        # run svn info once, so we create ~/.subversion/config
        run('svn info')
        output = run('cat %s' % svn_config)
    lines = output.split('\n')
    new_lines = []
    changed = False
    for line in lines:
        if 'store-passwords = no' in line:
            changed = True
            new_lines.append('store-passwords = no')
        else:
            new_lines.append(line)
    if changed:
        with settings(hide('running', 'stdout', 'stderr')):
            run('echo -e "{content}" > {config}'.format(
                content='\n'.join(new_lines), config=svn_config))


def _git_update(is_git=True):
    if not is_git:
        with cd(VENV):
            run('git clone --no-checkout git@github.com:Jarn/intranett.git gittmp')
            run('mv gittmp/.git/ .')
            run('rmdir gittmp')
            run('git reset --hard HEAD')

    run('git fetch')
    run('git remote prune origin')
    run('git gc')
    branch = env.server.config.get('branch', 'latest-tag')
    if branch == 'latest-tag':
        tag = _latest_git_tag()
    else:
        tag = 'origin/' + branch
    print('Switching to version: %s' % tag)
    with cd(VENV):
        run('git checkout -q --force %s' % tag)
        run('git reset --hard HEAD')
        run('git clean -fd')


def _is_git_repository():
    out = ''
    with settings(hide('stdout', 'stderr', 'warnings'), warn_only=True):
        with cd(VENV):
            out = run('git branch')
    return 'master' in out


def _latest_git_tag():
    output = run('git tag -l')
    tags = [t.rstrip('/') for t in output.split('\n')]
    tags = [(pkg_resources.parse_version(t), t) for t in tags]
    tags.sort()
    return tags[-1][1]


def _prepare_update(newest=True):
    envvars = _set_environment_vars()
    dump_db()
    _git_update()
    _buildout(envvars=envvars, newest=newest)


def _set_cron_mailto():
    with settings(hide('stdout', 'warnings'), warn_only=True):
        # if no crontab exists, this crontab -l has an exit code of 1
        run('crontab -l > %s/crontab.tmp' % HOME)
        crontab = run('cat %s/crontab.tmp' % HOME)
    cron_lines = crontab.split('\n')
    mailto = [l for l in cron_lines if l.startswith('MAILTO')]
    wrong_address = not CRON_MAILTO in mailto
    if not mailto or wrong_address:
        # add mailto right after the comments
        boilerplate = ('DO NOT EDIT THIS FILE', 'installed on',
            'Cron version V5.0')
        new_cron_lines = []
        added = False
        for line in cron_lines:
            if line.startswith('#'):
                # Remove some excessive boilerplate
                skip = False
                for b in boilerplate:
                    if b in line:
                        skip = True
                if not skip:
                    new_cron_lines.append(line)
            elif line.startswith('MAILTO') and wrong_address:
                continue
            else:
                if not added:
                    new_cron_lines.append('MAILTO=%s' % CRON_MAILTO)
                    added = True
                new_cron_lines.append(line)
        if not added:
            new_cron_lines.append('MAILTO=%s' % CRON_MAILTO)
        with settings(hide('running', 'stdout', 'stderr')):
            run('echo -e "{content}" > {home}/crontab.tmp'.format(
                home=HOME, content='\n'.join(new_cron_lines)))
            run('crontab %s/crontab.tmp' % HOME)
    with settings(hide('stdout', 'stderr')):
        run('rm %s/crontab.tmp' % HOME)


def _set_environment_vars():
    with settings(hide('stdout', 'stderr')):
        profile = run('cat %s/.bash_profile' % HOME)
    profile_lines = profile.split('\n')
    subdomain = env.host_string
    domain_line = 'export INTRANETT_DOMAIN=%s.intranett.no' % subdomain
    with settings(hide('stdout', 'stderr')):
        front_ip = run('/sbin/ifconfig ethfe | head -n 2 | tail -n 1')
    front_ip = front_ip.lstrip('inet addr:').split()[0]
    front_line = 'export INTRANETT_ZOPE_IP=%s' % front_ip

    exports = [l for l in profile_lines if l.startswith('export INTRANETT_')]
    if len(exports) < 2:
        start, end = profile_lines[:2], profile_lines[2:]
        new_file = start + [front_line] + [domain_line + '\n'] + end
        with settings(hide('running', 'stdout', 'stderr')):
            # run(domain_line)
            # run(front_line)
            run('echo -e "{content}" > {home}/.bash_profile'.format(
                home=HOME, content='\n'.join(new_file)))
    return dict(domain=domain_line, front=front_line)


def _setup_ssh_keys():
    with cd(HOME):
        with settings(hide('warnings'), warn_only=True):
            run('[ ! -e .ssh ] && mkdir .ssh && chmod 711 .ssh')
        ssh_dir = os.path.join(BUILDOUT_ROOT, 'etc', 'ssh')
        put("%s/id*" % ssh_dir, ".ssh/")
        run('chmod 600 .ssh/id_rsa')
        run('chmod 644 .ssh/id_rsa.pub')
        # add github to known hosts
        hosts = run("[ -e {hosts} ] && cat {hosts} || echo ''".format(
            hosts='.ssh/known_hosts'))
        host_lines = hosts.split('\n')
        github = any([l for l in host_lines if l.startswith('github.com')])
        if not github:
            put("%s/known_hosts" % ssh_dir, ".ssh/")


def _virtualenv():
    with settings(hide('stdout', 'stderr')):
        with cd(HOME):
            with settings(hide('warnings'), show('stdout'), warn_only=True):
                run('virtualenv-2.6 --no-site-packages --distribute %s' % VENV)
        run('rm -rf /tmp/distribute*')
        with cd(VENV):
            run('bin/easy_install-2.6 distribute==%s' % DISTRIBUTE_VERSION)
            with settings(hide('warnings', 'running'), warn_only=True):
                run('rm bin/activate')
                run('rm bin/activate_this.py')
                run('rm bin/pip')
            # Only install PIL if it isn't there
            with settings(hide('warnings', 'running'), show('stdout'),
                          warn_only=True):
                out = run('bin/python -c "from PIL import Image; '
                    'print(\'PIL: %s\' % Image.__version__)"')
            if PIL_VERSION not in out:
                with settings(show('stdout')):
                    run('bin/easy_install-2.6 %s' % PIL_LOCATION)
            with settings(hide('warnings', 'running'), warn_only=True):
                run('rm bin/pil*.py')
