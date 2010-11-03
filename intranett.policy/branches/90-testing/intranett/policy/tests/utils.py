from ZPublisher.HTTPRequest import FileUpload


class DummyFieldStorage(object):

    def __init__(self, data, filename, headers):
        self.file = data
        self.filename = filename
        self.headers = headers


def make_file_upload(data, content_type=None, filename=None):
    headers = {}
    if isinstance(data, str):
        data = open(data, 'rb')
    if content_type:
        headers['content-type'] = content_type
    fs = DummyFieldStorage(data, filename, headers)
    return FileUpload(fs)
