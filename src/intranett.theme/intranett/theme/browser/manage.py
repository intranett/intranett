from plone.app.portlets.browser.manage import ManageContextualPortlets


class IntranettManageContextualPortlets(ManageContextualPortlets):

    def __init__(self, context, request):
        # Note that we omit our own super class
        super(ManageContextualPortlets, self).__init__(context, request)
