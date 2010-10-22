from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.users.browser.personalpreferences import UserDataPanel,\
    UserDataConfiglet

class CustomUserDataPanel(UserDataPanel):
    """This overrides p.a.u. UserDataPanel to modify the bio widget.
    """

    def __init__(self, context, request):
        super(CustomUserDataPanel, self).__init__(context, request)
        self.form_fields['description'].custom_widget = WYSIWYGWidget


class CustomUserDataConfiglet(UserDataConfiglet):
    """This overrides p.a.u. UserDataPanel to modify the bio widget.
    """

    def __init__(self, context, request):
        super(CustomUserDataConfiglet, self).__init__(context, request)
        self.form_fields['description'].custom_widget = WYSIWYGWidget