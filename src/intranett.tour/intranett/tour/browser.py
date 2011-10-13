from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.amberjack.core")
PMF = MessageFactory('plone')

class AmberjackDefaults(BrowserView): 
    def __call__(self, context, request):
        constants = """
            if (AmberjackPlone){
                AmberjackPlone.aj_plone_consts['Error'] = "%s";
                AmberjackPlone.aj_plone_consts['ErrorValidation'] = "%s";
                AmberjackPlone.aj_plone_consts['BrowseFile'] = "%s";
                AmberjackPlone.aj_plone_consts['AlertDefaultTitle'] = "%s";
                AmberjackPlone.aj_plone_consts['AlertDisableLinksMessage'] = "%s";
                AmberjackPlone.aj_plone_consts['GoToNextStepLinkMessage'] = "%s";
                AmberjackPlone.aj_plone_consts['GoToNextStepLinkErrorMessage'] = "%s";
                AmberjackPlone.aj_plone_consts['FieldRequiredErrorMessage'] = "%s";
            }
        """ % (translate(PMF(u'Error'), context=self.request),
               translate(PMF(u'Please correct the indicated errors.'), context=self.request),
               translate(_(u'Please select a file.'), context=self.request),
               translate(_(u'Amberjack alert'), context=self.request),
               translate(_(u"You cannot click on other links, please use the console's exit button."), context=self.request),
               translate(_(u"Go to next step automatically."), context=self.request),
               translate(_(u"Can't go to next step automatically. Do it manually."), context=self.request),
               translate(_(u"This field is required, please correct."), context=self.request)
               )
        portal_url = self.context.portal_url()
        return """
        function loadDefaults(){
            Amberjack.onCloseClickStay = true;
            Amberjack.doCoverBody = false;
            Amberjack.PORTAL_URL = '%s/';
            Amberjack.textOf = "%s";
            Amberjack.BASE_URL = $('#personal-folder-link').attr('href');
            %s
        }
        """  % (portal_url,
                translate(_('separator-between-steps', default=u"of"), context=self.request),
                constants)