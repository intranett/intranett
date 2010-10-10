from plone.app.portlets.browser.manage import ManageContextualPortlets

class IntranettManageContextualPortlets(ManageContextualPortlets):

    def __init__(self, context, request):
        super(ManageContextualPortlets, self).__init__(context, request)