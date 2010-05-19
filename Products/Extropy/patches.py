from plone.app.linkintegrity import handlers

def _null_handler(obj, event):
    return

handlers.modifiedArchetype = _null_handler
handlers.referenceRemoved = _null_handler
handlers.referencedObjectRemoved = _null_handler


from Products.CMFPlone.patches.unicodehacks import FasterStringIO
from chameleon.core import generation

def initialize_stream():
    out = FasterStringIO()
    return (out, out.write)

generation.initialize_stream = initialize_stream
