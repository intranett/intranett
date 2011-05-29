from Products.Extropy.permissions import *

PROJECTNAME = "Extropy"

TOOLNAME = 'extropy_tracking_tool'
TOOLTYPE = 'Extropy Tracking Tool'

TIMETOOLNAME = 'extropy_timetracker_tool'
TIMETOOLTYPE = 'Extropy TimeTracker Tool'

GLOBALS = globals()

OPEN_STATES = ['open', 'in-progress','active','unassigned','deferred','assigned','testing','taskscomplete']

# TIMETRACKING

WORKTYPES=('development', 'administration', 'managing', 'user-interface')

DEFAULT_BUGDET_CATEGORIES = (('Billable','Billable'),
                             ('Administration', 'Administration'),
                             ('SkillAndBrand','Skill and brand investment'),
                             ('Sales','Sales')
                             )

BILLABLE_TYPES = (
    'ExtropyActivity',
    'Contract',
    )
