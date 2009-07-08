from Products.CMFCore.utils import ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import ToolInit

from Products.Archetypes.public import process_types, listTypes

from Products.Extropy.config import *
from Products.Extropy import tools

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    from Products.Extropy import content

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)

    TOOLS = (
        tools.ExtropyTimeTrackerTool.ExtropyTimeTrackerTool,
        tools.ExtropyTrackingTool.ExtropyTrackingTool,
        )
    ToolInit(
        PROJECTNAME + ' Tool',
        tools = TOOLS,
        icon = 'tool.gif',
        ).initialize(context)

    import patches
