import json

from zope.publisher.browser import BrowserView

from intranett.policy.config import config


class SystemInfo(BrowserView):

    def __call__(self):
        output = {'version': config.package_version}
        return json.dumps(output)
