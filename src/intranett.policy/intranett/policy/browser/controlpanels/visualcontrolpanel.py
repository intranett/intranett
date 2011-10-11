from plone.app.registry.browser import controlpanel

from intranett.policy.browser.controlpanels.interfaces import IVisualSettings, _


class VisualSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IVisualSettings
    label = _(u"Visual settings")
    description = _(u"""""")

    def updateFields(self):
        super(VisualSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(VisualSettingsEditForm, self).updateWidgets()

class VisualSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = VisualSettingsEditForm