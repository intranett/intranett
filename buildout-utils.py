# Workaround for https://bugs.launchpad.net/zc.buildout/+bug/164629

def patchScriptGeneration(buildout):
    from zc.buildout import easy_install
    if not 'sys.exit(' in easy_install.script_template:
        easy_install.script_template = easy_install.script_template.replace(
            "%(module_name)s.%(attrs)s(%(arguments)s)",
            "sys.exit(%(module_name)s.%(attrs)s(%(arguments)s))")
