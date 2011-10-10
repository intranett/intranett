from Acquisition import aq_inner


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


def check_quick_upload_locally_addable():
    from collective.quickupload.portlet.quickuploadportlet import Renderer

    def available(self):
        context = aq_inner(self.context)
        allowed_types = context.getLocallyAllowedTypes()
        return self._old_available and ('File' in allowed_types or 'Image' in allowed_types)
    Renderer._old_available = Renderer.available
    Renderer.available = available

def apply():
    allow_anonymous()
    optimize_rr_packing()
    check_quick_upload_locally_addable()