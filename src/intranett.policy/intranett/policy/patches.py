def allow_anonymous():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('robots.txt')
    addValidIds('logged_out')
    addValidIds('system-info')
    addValidSubparts('portal_kss')


def allow_anonymous_activation():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('activate_form')
    addValidSubparts('activate')


def optimize_rr_packing():
    from Products.ResourceRegistries.tools import CSSRegistry
    from Products.ResourceRegistries.tools import JSRegistry
    from Products.ResourceRegistries.tools import KSSRegistry
    from .compress import css, js
    CSSRegistry.CSSRegistryTool._compressCSS = css
    JSRegistry.JSRegistryTool._compressJS = js
    KSSRegistry.KSSRegistryTool._compressKSS = css


def apply():
    allow_anonymous()
    allow_anonymous_activation()
    optimize_rr_packing()
