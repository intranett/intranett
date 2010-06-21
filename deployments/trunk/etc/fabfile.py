from fabric.api import env


env.reject_unknown_hosts = True
env.disable_known_hosts = True
env.shell = "/bin/bash -c"


def dummy():
    print "Works!"
