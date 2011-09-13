from email.Header import Header

from AccessControl import ModuleSecurityInfo
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView

from intranett.policy import IntranettMessageFactory as _


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


def loginUser(context, userid, password):
    """Called from activate_action."""
    membership = getToolByName(context, 'portal_membership')
    utils = getToolByName(context, 'plone_utils')
    member = membership.getMemberById(userid)
    if member is not None:
        newSecurityManager(None, member.getUser())
        context.REQUEST.set('__ac_password', password)
        context.logged_in()
        utils.addPortalMessage(_(u'Welcome! You are now logged in.'))


# Allow from Python scripts
security = ModuleSecurityInfo('intranett.policy.browser.activation')
security.declarePublic('loginUser')
