from fabric.api import cd, env, run, sudo

env.shell = "/bin/bash -c"

def touch():
    home = run('pwd')
    run('cd {home} && touch iwashere.txt'.format(home=home))

def svn_info():
    with cd('/srv/jarn'):
        sudo('pwd && svn info', user='jarn')
