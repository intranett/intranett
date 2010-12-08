import sys

from StringIO import StringIO
from ZPublisher.HTTPRequest import FileUpload


class DummyFieldStorage(object):
    """Minimal FieldStorage implementation."""

    def __init__(self, data, filename, headers):
        self.file = data
        self.filename = filename
        self.headers = headers


def make_file_upload(data, content_type=None, filename=None):
    """Create a FileUpload object.
    """
    headers = {}
    if isinstance(data, str):
        data = open(data, 'rb')
    if content_type:
        headers['content-type'] = content_type
    fs = DummyFieldStorage(data, filename, headers)
    return FileUpload(fs)


def suppress_warnings(func):
    """Decorator suppressing stderr output.
    """
    def wrapped_func(*args, **kw):
        saved = sys.stderr
        try:
            sys.stderr = StringIO()
            return func(*args, **kw)
        finally:
            sys.stderr = saved

    wrapped_func.__name__ = func.__name__
    wrapped_func.__module__ = func.__module__
    wrapped_func.__doc__ = func.__doc__
    wrapped_func.__dict__.update(func.__dict__)
    return wrapped_func
