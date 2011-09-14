from urllib import quote
from email import message_from_string
from email.Header import Header

from zope.interface import Interface
from zope import schema

from AccessControl import ModuleSecurityInfo
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PloneInvite.browser.register import InviteRegistrationForm
from zope.formlib import form, widget
from zope.publisher.browser import BrowserView

from intranett.policy import IntranettMessageFactory as _


class InvitationMail(BrowserView):

    index = ViewPageTemplateFile('templates/invitation-mail.pt')

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


def sendInvitationMail(site, member, vars):
    fullname = member.getProperty('fullname') or member.getId()
    hostname = site.REQUEST.SERVER_NAME
    invite_to_address = vars['invite_to_address']
    enforce_address = vars['enforce_address']
    invitecode = vars['invitecode']
    message = vars['message']

    tool = getToolByName(site, 'portal_invitations')
    expires = DateTime() + tool.getProperty('days', 7)

    accept_url = '%s/accept?code=%s&email=%s' % (
        site.absolute_url(), quote(invitecode), quote(invite_to_address))

    mail_text = InvitationMail(site, site.REQUEST)(member=member,
        email=invite_to_address, sender_fullname=fullname, hostname=hostname,
        message=message, expires=expires, accept_url=accept_url)
    if isinstance(mail_text, unicode):
        mail_text = mail_text.encode('utf-8')

    message_obj = message_from_string(mail_text.strip())
    subject = message_obj['Subject']
    m_to = message_obj['To']
    m_from = message_obj['From']

    host = getToolByName(site, 'MailHost')
    host.send(mail_text, m_to, m_from, subject=subject,
              charset='utf-8', immediate=True)


# Allow from Python scripts
security = ModuleSecurityInfo('intranett.policy.browser.invitation')
security.declarePublic('sendInvitationMail')


class AcceptForm(InviteRegistrationForm):

    description = u""

    @property
    def form_fields(self):
        """Insert the 'invite_code' field."""
        fields = super(AcceptForm, self).form_fields
        # Move invite_code field up one slot
        fields.__FormFields_seq__ = (
            fields.__FormFields_seq__[:-2] +
            fields.__FormFields_seq__[-1:] +
            fields.__FormFields_seq__[-2:-1])
        return fields

    def __call__(self):
        code = self.request.get('code')
        if code:
            self.request.form['form.invite_code'] = code
        email = self.request.get('email')
        if email:
            self.request.form['form.email'] = email
        return super(AcceptForm, self).__call__()

