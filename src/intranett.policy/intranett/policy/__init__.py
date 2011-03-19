import patches
from zope.i18nmessageid import MessageFactory

IntranettMessageFactory = MessageFactory('intranett')

patches.apply()

# Register content
import content.membersfolder


def initialize(context):
    from intranett.policy.config import config
    config.register_profile()
    config.scan()

    from AccessControl import allow_module
    allow_module('intranett.policy.config')

    from Products.Archetypes import atapi
    from Products.CMFCore import utils
    from intranett.policy import config

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types = (atype,),
            permission = config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)
