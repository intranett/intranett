from Products.CMFCore.utils import ContentInit
from Products.CMFCore.utils import ToolInit

from Products.Archetypes.public import process_types, listTypes

from Products.Extropy import config
from Products.Extropy import tools

def initialize(context):
    from Products.Extropy import content

    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME), config.PROJECTNAME)

    ContentInit(
        config.PROJECTNAME + ' Content',
        content_types = content_types,
        permission = config.ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        ).initialize(context)

    TOOLS = (
        tools.ExtropyTimeTrackerTool.ExtropyTimeTrackerTool,
        tools.ExtropyTrackingTool.ExtropyTrackingTool,
        )
    ToolInit(
        config.PROJECTNAME + ' Tool',
        tools = TOOLS,
        icon = 'tool.gif',
        ).initialize(context)

    import patches
