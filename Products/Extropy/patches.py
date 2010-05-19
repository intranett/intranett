from plone.app.linkintegrity import handlers

def _null_handler(obj, event):
    return

handlers.modifiedArchetype = _null_handler
handlers.referenceRemoved = _null_handler
handlers.referencedObjectRemoved = _null_handler
