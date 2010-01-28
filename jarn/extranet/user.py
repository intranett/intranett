from Acquisition import aq_inner, aq_chain
from plone.memoize.instance import memoize
from zope.interface import implements
from jarn.extranet.interfaces import ICustomer
from Products.membrane.interfaces.user import IMembraneUserObject


class UserIdProvider(object):
    """
    Adapts from SimpleMember to IMembraneUserObject.  Uses a massaged path to
    the member object instead of the UID.
    """
    implements(IMembraneUserObject)

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        return self.context.getUserName()

    def getUserName(self):
        return self.context.getUserName()



