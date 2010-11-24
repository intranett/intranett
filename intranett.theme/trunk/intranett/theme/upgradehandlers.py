import logging

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('intranett.theme upgrades')


def add_media_query_maincss(context):
    css = getToolByName(context, 'portal_css')
    main = css.getResource('main.css')
    main.setMedia("")


def add_selectivizr_remove_html5_js(context):
    js = getToolByName(context, 'portal_javascripts')
    ids = js.getResourcesDict().keys()
    # remove html5.js
    if 'html5.js' in ids:
        js.unregisterResource('html5.js')
    # add selectivizr.js
    if 'selectivizr.js' not in ids:
        js.registerScript('selectivizr.js')

    sel = js.getResource('selectivizr.js')
    sel.setConditionalcomment('lt IE 9')
    js.moveResourceAfter('selectivizr.js', 'jquery.js')
    js.cookResources()
