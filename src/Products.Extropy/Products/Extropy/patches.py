from plone.app.linkintegrity import handlers

def _null_handler(obj, event):
    return

handlers.modifiedArchetype = _null_handler
handlers.referenceRemoved = _null_handler
handlers.referencedObjectRemoved = _null_handler


try:
    from chameleon.core import generation
    from Products.CMFPlone.patches.unicodehacks import FasterStringIO
except ImportError:
    pass
else:
    def initialize_stream():
        out = FasterStringIO()
        return (out, out.write)

    generation.initialize_stream = initialize_stream
