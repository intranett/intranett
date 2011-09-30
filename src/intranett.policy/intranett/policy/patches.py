def allow_anonymous_robotstxt():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('robots.txt')
    addValidIds('logged_out')
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
    allow_anonymous_robotstxt()
    allow_anonymous_activation()
    optimize_rr_packing()


def no_plonesite_quick_upload():
    # Remove IQuickUploadCapable from PloneSite, so the portlet does not show
    # up in control panels or other `contentless` places
    from Products.CMFPlone.Portal import PloneSite
    from collective.quickupload.browser.interfaces import IQuickUploadCapable
    from zope.interface import classImplementsOnly, implementedBy
    spec = implementedBy(PloneSite)
    declared = spec.declared
    if IQuickUploadCapable in declared:
        new_decl = tuple([d for d in declared if d is not IQuickUploadCapable])
        classImplementsOnly(new_decl)


def after_zcml():
    no_plonesite_quick_upload()
