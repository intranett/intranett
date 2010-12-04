from fabric.api import env, run

env.shell = "/bin/bash -c"

def touch():
    home = run('pwd')
    run('cd {home} && touch iwashere.txt'.format(home=home))
