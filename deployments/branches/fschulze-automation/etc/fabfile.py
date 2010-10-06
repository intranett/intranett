import fabric.main
from fabric.api import cd, env, sudo


env.reject_unknown_hosts = True
env.disable_known_hosts = True
env.shell = "/bin/bash -c"


def run(command, shell=True, pty=False):
    orig_cwd = cwd = env.get('cwd', '')
    if cwd == '':
        cwd = '~/'
    print cwd
    if cwd.startswith('~/'):
        cwd = '/srv/jarn/%s' % cwd[2:]
    print cwd
    env['cwd'] = cwd
    result = sudo(command, shell=shell, user="jarn", pty=pty)
    env['cwd'] = orig_cwd
    return result
fabric.main._internals.append(run)


def dummy():
    run("pwd")
    run("ls")
    with cd("~/eggs"):
        run("ls")