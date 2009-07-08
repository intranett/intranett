from Products.CMFCore.utils import ContentInit
from Products.CMFCore.DirectoryView import registerDirectory

from Products.Archetypes.public import listTypes
from Products.Archetypes.public import process_types

from Products.Invoice import config
from Products.Invoice import permissions

registerDirectory(config.SKINS_DIR, config.GLOBALS)

def initialize(context):

    from Products.Invoice import content

    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME), config.PROJECTNAME)

    ContentInit(
        config.PROJECTNAME + ' Content',
        content_types = content_types,
        permission = permissions.ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
    ).initialize(context)
