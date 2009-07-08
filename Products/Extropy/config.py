from Products.Extropy.permissions import *
from Products.Archetypes.public import DisplayList


PROJECTNAME = "Extropy"

TOOLNAME = 'extropy_tracking_tool'
TOOLTYPE = 'Extropy Tracking Tool'

TIMETOOLNAME = 'extropy_timetracker_tool'
TIMETOOLTYPE = 'Extropy TimeTracker Tool'

GLOBALS = globals()

SKINS_DIR = 'skins'

TASK_PRIORITIES = (('1','NiceToHave'),('5','Normal'),('10','Urgent'))

DEFAULT_WORKTYPES = ('Development',
                     'Planning/Managing',
                     'Paperwork',
                     'Mail',
                     'Meeting',
                     'User Interface',
                     'Design',
                     'Travel')

#HOUR = 1.0/24.0   # datetime stuff
WORKDAY = 6.0
TASK_ESTIMATES = (
                  (str(0.0)     ,'Not set'   ),
                  (str(0.25)     ,'a few minutes'   ),
                  (str(1.0)         ,'1 hour'          ),
                  (str(WORKDAY/2.0)  ,'half a day'      ),
                  (str(WORKDAY)        ,'1 day'           ),
                  )


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

BILLABLE_TYPES = ('ExtropyTask', 'ExtropyActivity', 'ExtropyFeature')

PLAN_RELATIONSHIP = 'plannedItem'
PLAN_ADDITIONAL_RELATIONSHIP = 'adHocItem'
PLAN_TARGET_STATES = ('completed',)

INVOICE_RELATIONSHIP = 'invoice'
