def allow_anonymous():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('activate_form')
    addValidIds('logged_out')
    addValidIds('robots.txt')
    addValidIds('system-info')
    addValidSubparts('activate')
    addValidSubparts('portal_kss')


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
    optimize_rr_packing()
