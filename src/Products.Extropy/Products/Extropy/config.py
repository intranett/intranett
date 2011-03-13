from Products.Extropy.permissions import *

PROJECTNAME = "Extropy"

TOOLNAME = 'extropy_tracking_tool'
TOOLTYPE = 'Extropy Tracking Tool'

TIMETOOLNAME = 'extropy_timetracker_tool'
TIMETOOLTYPE = 'Extropy TimeTracker Tool'

GLOBALS = globals()

TASK_PRIORITIES = (('1','NiceToHave'),('5','Normal'),('10','Urgent'))

DEFAULT_WORKTYPES = ('Development',
                     'Planning/Managing',
                     'Paperwork',
                     'Mail',
                     'Meeting',
                     'User Interface',
                     'Design',
                     'Travel')

WORKDAY = 6.0

TASK_FOR_RELATIONSHIP = 'taskFor'
ORIGINATING_TASK_RELATIONSHIP = 'originatingTask'

ROLES = ('Participant',)

OPEN_STATES = ['open', 'in-progress','active','unassigned','deferred','assigned','testing','taskscomplete']

# TIMETRACKING

WORKTYPES=('development', 'administration', 'managing', 'user-interface')

DEFAULT_BUGDET_CATEGORIES = (('Billable','Billable'),
                             ('Administration', 'Administration'),
                             ('SkillAndBrand','Skill and brand investment'),
                             ('Sales','Sales')
                             )

BILLABLE_TYPES = (
    'ExtropyTask',
    'ExtropyActivity',
    'ExtropyFeature',
    'Contract',
    )

PLAN_RELATIONSHIP = 'plannedItem'
PLAN_ADDITIONAL_RELATIONSHIP = 'adHocItem'
PLAN_TARGET_STATES = ('completed',)

INVOICE_RELATIONSHIP = 'invoice'
