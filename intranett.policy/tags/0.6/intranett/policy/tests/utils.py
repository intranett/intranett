from ZPublisher.HTTPRequest import FileUpload


class DummyFieldStorage:

    def __init__(self, file, filename, headers):
        self.file = file
        self.filename = filename
        self.headers = headers


def makeFileUpload(file, content_type=None, filename=None):
    headers = {}
    if type(file) == type(''):
        file = open(file, 'rb')
    if content_type:
        headers['content-type'] = content_type
    fs = DummyFieldStorage(file, filename, headers)
    return FileUpload(fs)