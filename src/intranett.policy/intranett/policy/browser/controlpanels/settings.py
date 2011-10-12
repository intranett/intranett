from zope import schema
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.site.hooks import getSite
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFPlone.utils import safe_unicode

from intranett.policy import IntranettMessageFactory

_ = IntranettMessageFactory



class ISettings(Interface):
    """Global visual settings.
    """

    site_title = schema.TextLine(title=_(u"Intranet name"),
                                  description=_(u"help_akismet_key_site",
                                                default=u"Enter the name of your intranett, this will be used as the title of your intranet and also in place of a logo if you do not have a logo"),
                                  required=False,
                                  default=u'',)

class SettingsAdapter(SchemaAdapterBase):   
    adapts(IPloneSiteRoot)
    implements(ISettings)
    def __init__(self, context):
        super(SettingsAdapter, self).__init__(context)
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.site_properties
        self.encoding = pprop.site_properties.default_charset

    def get_site_title(self):
        title = getattr(self.portal, 'title', u'')
        return safe_unicode(title)

    def set_site_title(self, value):
        self.portal.title = value.encode(self.encoding)


    site_title = property(get_site_title, set_site_title)

 
class SettingsControlPanel(ControlPanelForm):

    form_fields = form.FormFields(ISettings)
    
    label = _("Settings")
    description = _("")
    form_name = _("")

