from zope.i18nmessageid import MessageFactory
from jarn.extranet import config

from Products.Archetypes import atapi
from Products.CMFCore import utils

_ = MessageFactory('Extropy')


def initialize(context):
    import jarn.extranet.customer
    import jarn.extranet.contract

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.meta_type),
            content_types      = (atype,),
            permission         = config.ADD_PERMISSIONS[atype.meta_type],
            extra_constructors = (constructor,),
            ).initialize(context)
