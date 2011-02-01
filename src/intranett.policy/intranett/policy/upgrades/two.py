import logging

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('intranett.policy')


def two_to_three(context):
    url_tool = getToolByName(context, 'portal_url')
    site = url_tool.getPortalObject()
    existing_roles = set(getattr(site, '__ac_roles__', []))
    existing_roles.add('Site Administrator')
    site.__ac_roles__ = tuple(existing_roles)

    context.runImportStepFromProfile('profile-intranett.policy:default',
                                     'rolemap')
    context.runImportStepFromProfile('profile-intranett.policy:default',
                                     'actions')
    logger.info('Added Site Administrator role/actions.')
