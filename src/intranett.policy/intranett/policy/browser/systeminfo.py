import json

from zope.publisher.browser import BrowserView

from intranett.policy.config import config


class SystemInfo(BrowserView):

    def __call__(self):
        output = {'version': config.package_version}
        self.request.response.setHeader('content-type', 'application/json')
        self.request.response.setBody(json.dumps(output))
        return self.request.response
