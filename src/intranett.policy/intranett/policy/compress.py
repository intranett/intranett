import hashlib
import os
import os.path
import subprocess

BUILDOUT_ROOT = None
RESOURCE_DIR = None
YUI_PATH = None


def _get_paths():
    global BUILDOUT_ROOT, RESOURCE_DIR, YUI_PATH
    if BUILDOUT_ROOT is None:
        BUILDOUT_ROOT = os.environ.get('BUILDOUT_ROOT')
        if not BUILDOUT_ROOT:
            return None, None
    if RESOURCE_DIR is None:
        RESOURCE_DIR = os.path.join(BUILDOUT_ROOT, 'var', 'resources')
    if YUI_PATH is None:
        YUI_PATH = os.path.join(
            BUILDOUT_ROOT, 'tools', 'yuicompressor-2.4.6.jar')
    return RESOURCE_DIR, YUI_PATH


def _compress(content, format, level=None):
    res_dir, yui_path = _get_paths()
    if res_dir is None:
        return content
    if isinstance(content, unicode):
        content = content.encode('ascii', 'ignore')
    digest = hashlib.sha1(content).hexdigest()
    cache_path = os.path.join(res_dir, digest)
    if os.path.isfile(cache_path):
        with open(cache_path, 'rb') as fp:
            result = fp.read()
        return result.decode('ascii', 'ignore')
    args = ['java', '-jar', yui_path, '--type=%s' % format]
    process = subprocess.Popen(args,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate(input=content)
    del process
    result = out.decode('ascii', 'decode')
    with open(cache_path, 'wb') as fp:
        fp.write(result)
        fp.flush()
    return result


def css(self, content, level='safe'):
    if not level:
        return content
    return _compress(content, 'css', level=level)


def js(self, content, level='safe'):
    if not level:
        return content
    return _compress(content, 'js', level=level)
