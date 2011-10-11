from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory

from intranett.policy import IntranettMessageFactory

_ = IntranettMessageFactory


class IVisualSettings(Interface):
    """Global visual settings.
    """

    customer_logo = schema.Bytes(title=_(u"Logo"),
                                  description=_(u"help_customer_logo",
                                                default=u"Upload your logo. Remember, we use your logo in the size it is uploaded."),
                                  required=False,)

    site_title = schema.TextLine(title=_(u"Intranet name"),
                                  description=_(u"help_akismet_key_site",
                                                default=u"Enter the name of your intranett"),
                                  required=False,
                                  default=u'',)