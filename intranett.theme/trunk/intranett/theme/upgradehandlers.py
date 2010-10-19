import logging

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('intranett.theme upgrades')


def null_upgrade_step(context):
    pass


def add_media_query_maincss(context):
    css = getToolByName(context, 'portal_css')
    main = css.getResource('main.css')
    main.setMedia("")
