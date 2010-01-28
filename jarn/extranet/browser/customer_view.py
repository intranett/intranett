from zope import component, interface, schema
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.i18n import translate


from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from jarn.extranet import MessageFactory as _

class CustomerView(BrowserView):
    pass        
        