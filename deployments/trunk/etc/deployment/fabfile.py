from fabric.api import env, run

env.shell = "/bin/bash -c"

def touch():
    home = run('pwd')
    run('cd {home} && touch iwashere.txt'.format(home=home))

def svn_info():
    home = run('pwd')
    run('cd {home} && svn info /srv/jarn'.format(home=home))
