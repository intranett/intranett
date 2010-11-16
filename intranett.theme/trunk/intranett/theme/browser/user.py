from zope.publisher.browser import BrowserView


class UserView(BrowserView):

    def username(self):
        return self.request.form.get('name', '')
