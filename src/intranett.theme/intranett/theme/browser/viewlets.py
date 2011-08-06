from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import LogoViewlet

class IntranettLogoViewlet(LogoViewlet):
    index = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()

        portal = self.portal_state.portal()
        bprops = portal.restrictedTraverse('base_properties', None)
        if bprops is not None:
            logoName = bprops.logoName
        else:
            logoName = 'logo.jpg'

        try:
            self.logo_tag = portal.restrictedTraverse(logoName).tag()
        except KeyError:
            self.logo_tag = False
        self.navigation_root_title = self.portal_state.navigation_root_title()