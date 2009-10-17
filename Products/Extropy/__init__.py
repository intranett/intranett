from AccessControl import allow_class
from AccessControl import allow_module

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.utils import ToolInit

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

    allow_module('Products.Extropy.odict')
    from Products.Extropy.odict import OrderedDict
    allow_class(OrderedDict)

    # What follows shoulnd't be required, but zope.i18n.locales is stupid
    from zope.i18n.locales import locales    
    gregorian = locales.getLocale('en').dates.calendars[u'gregorian']

    date_format = gregorian.dateFormats['medium'].formats[None]
    time_format = gregorian.timeFormats['medium'].formats[None]

    date_format.pattern = u'yyyy-MM-dd '
    time_format.pattern = u'HH:mm:ss '
