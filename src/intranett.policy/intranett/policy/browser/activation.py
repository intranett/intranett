from email.Header import Header

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView


class ActivationMail(BrowserView):

    index = ViewPageTemplateFile('templates/activation-mail.pt')

    def mail_header(self):
        site = getToolByName(self.context, 'portal_url').getPortalObject()
        from_ = site.getProperty('email_from_name')
        mail  = site.getProperty('email_from_address')
        text = '"%s" <%s>' % (from_, mail)
        return Header(safe_unicode(text), 'utf-8')

    def __call__(self, **kw):
        options = kw.copy()
        options['from_'] = self.mail_header()
        return self.index(**options)
