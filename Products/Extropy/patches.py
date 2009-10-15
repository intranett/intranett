from plone.memoize import forever

# Remember the installed products and packages
from App import FactoryDispatcher

FactoryDispatcher._product_packages = \
    forever.memoize(FactoryDispatcher._product_packages)


from plone.app.linkintegrity import handlers

def _null_handler(obj, event):
    return

handlers.modifiedArchetype = _null_handler
handlers.referenceRemoved = _null_handler
handlers.referencedObjectRemoved = _null_handler


def opaqueItems(self):
    """ We don't use no freaking comments """
    return ()

from Products.CMFCore.CMFCatalogAware import CMFCatalogAware

# We don't have any opaque items in the site, ignore those
CMFCatalogAware.originalOpaqueItems = CMFCatalogAware.opaqueItems
CMFCatalogAware.opaqueItems = opaqueItems


from plone.memoize import volatile

from Acquisition import ImplicitAcquisitionWrapper
from Products.Archetypes import BaseObject
from Products.Archetypes.interfaces import ISchema


_SCHEMA_CACHE = {}

def _schema_storage(fun, *args, **kwargs):
    return _SCHEMA_CACHE


def _schema_key(method, self, *args, **kwargs):
    return (self.__class__, self.portal_type)


@volatile.cache(_schema_key, _schema_storage)
def _raw_schema(self):
    return ISchema(self)


def _Schema(self):
    """Return a (wrapped) schema instance for this object instance.
    """
    schema = _raw_schema(self)
    return ImplicitAcquisitionWrapper(schema, self)


BaseObject.BaseObject.Schema = _Schema
