from zope.component import getUtility, getMultiAdapter, ComponentLookupError
from zope.component import getSiteManager
from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletType

import logging
logger  = logging.getLogger('intranett.theme upgrades')

def add_media_query_maincss(context):
    """"""
    css = getToolByName(context, 'portal_css')
    main = css.getResource('main.css')
    main.setMedia("")

