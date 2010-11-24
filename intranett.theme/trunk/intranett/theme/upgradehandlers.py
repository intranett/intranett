import logging

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('intranett.theme upgrades')


def add_media_query_maincss(context):
    css = getToolByName(context, 'portal_css')
    main = css.getResource('main.css')
    main.setMedia("")


def add_selectivizr_remove_html_js(context):
    js = getToolByName(context, 'portal_javascripts')
    # remove html5.js
    pass
    # add selectivizr.js conditionalcomment="lt IE 9" insert-after="jquery.js"
    pass
