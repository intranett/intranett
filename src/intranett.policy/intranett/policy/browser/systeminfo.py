import json

from Acquisition import aq_get
from BTrees.IIBTree import multiunion
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView

from intranett.policy.config import config


class SystemInfo(BrowserView):

    def __call__(self):
        context = self.context
        acl_users = aq_get(context, 'acl_users')
        catalog = getToolByName(context, 'portal_catalog')
        now = DateTime()
        modified = catalog._catalog.indexes['modified']
        mod_values = modified._index.values
        days_7 = modified._convert(now - 7)
        days_14 = modified._convert(now - 14)
        days_30 = modified._convert(now - 30)
        output = {
            'version': config.package_version,
            'objects': len(catalog),
            'users': len(acl_users.source_users.listUserIds()),
            'modified_30': len(multiunion(mod_values(days_30))),
            'modified_14': len(multiunion(mod_values(days_14))),
            'modified_7': len(multiunion(mod_values(days_7))),
        }
        response = self.request.response
        response.setHeader('content-type', 'application/json')
        response.setBody(json.dumps(output))
        return response
