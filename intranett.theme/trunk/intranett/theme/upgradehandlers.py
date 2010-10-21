import logging

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('intranett.theme upgrades')


def add_media_query_maincss(context):
    css = getToolByName(context, 'portal_css')
    main = css.getResource('main.css')
    main.setMedia("")
    
def add_personslisting_action(context):
    # at = getToolByName(self.portal, 'portal_actions')
    # tabs = at.portal_tabs
    # 'persons-listing' in tabs.objectIds()
