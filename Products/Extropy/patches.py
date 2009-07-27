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
